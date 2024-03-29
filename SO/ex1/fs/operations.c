#include "operations.h"
#include "config.h"
#include "state.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/types.h>
#include "betterassert.h"

tfs_params tfs_default_params() {
    tfs_params params = {
        .max_inode_count = 64,
        .max_block_count = 1024,
        .max_open_files_count = 16,
        .block_size = 1024,
    };
    return params;
}

int tfs_init(tfs_params const *params_ptr) {

    tfs_params params;
    if (params_ptr != NULL) {
        params = *params_ptr;
    } else {
        params = tfs_default_params();
    }

    if (state_init(params) != 0) {
        return -1;
    }

    // create root inode
    int root = inode_create(T_DIRECTORY);
    if (root != ROOT_DIR_INUM) {
        return -1;
    }


    return 0;
}

int tfs_destroy() {
    if (state_destroy() != 0) {
        return -1;
    }
    return 0;
}

static bool valid_pathname(char const *name) {
    return name != NULL && strlen(name) > 1 && name[0] == '/';
}

/**
 * Looks for a file.
 *
 * Note: as a simplification, only a plain directory space (root directory only)
 * is supported.
 *
 * Input:
 *   - name: absolute path name
 *   - root_inode: the root directory inode
 * Returns the inumber of the file, -1 if unsuccessful.
 */
static int tfs_lookup(char const *name, inode_t *root_inode) {
    
    // assert that root_inode is the root directory
    inode_t *root_dir_inode = inode_get(ROOT_DIR_INUM);
    ALWAYS_ASSERT(root_dir_inode != NULL, "tfs_lookup: root dir inode must exist");
    if (root_dir_inode != root_inode) {
        return -1;
    }
    if (!valid_pathname(name)) {
        return -1;
    }

    // skip the initial '/' character
    name++;

    return find_in_dir(root_inode, name);
}

int tfs_open(char const *name, tfs_file_mode_t mode) {
    // Checks if the path name is valid
    if (!valid_pathname(name)) {
        return -1;
    }

    inode_t *root_dir_inode = inode_get(ROOT_DIR_INUM);
    ALWAYS_ASSERT(root_dir_inode != NULL, "tfs_open: root dir inode must exist");

    int inum = tfs_lookup(name, root_dir_inode);
    size_t offset;

    // The file already exists
    if (inum >= 0) {
        inode_t *inode = inode_get(inum);

        // lock the inode
        pthread_rwlock_wrlock(&inode_locks[inum]);
        ALWAYS_ASSERT(inode != NULL, "tfs_open: directory files must have an inode");

        if(inode->i_node_type == T_SYMLINK) {
            char *data = data_block_get(inode->i_data_block);
            //unlock the inode
            pthread_rwlock_unlock(&inode_locks[inum]);
            return tfs_open(data, mode); 
        }

        // Truncate (if requested)
        if (mode & TFS_O_TRUNC) {
            if (inode->i_size > 0) {
                data_block_free(inode->i_data_block);
                inode->i_size = 0;
            }
        }
        // Determine initial offset
        if (mode & TFS_O_APPEND) {
            offset = inode->i_size;
        } else {
            offset = 0;
        }

        //unlock the inode
        pthread_rwlock_unlock(&inode_locks[inum]);
        
    // The file does not exist; the mode specified that it should be created
    } else if (mode & TFS_O_CREAT) {
        // Create inode
        inum = inode_create(T_FILE);
        if (inum == -1) {
            // no space in inode table
            return -1; 
        }

        // Add entry in the root directory
        if (add_dir_entry(root_dir_inode, name + 1, inum) == -1) {
            // no space in directory
            inode_delete(inum);
            return -1; 
        }

        offset = 0;
    } else {
        return -1;
    }

    // Finally, add entry to the open file table and return the corresponding
    // handle
    int handle = add_to_open_file_table(inum, offset);
    if (handle == -1) {
        return -1;
    }
    return handle;

    // Note: for simplification, if file was created with TFS_O_CREAT and there
    // is an error adding an entry to the open file table, the file is not
    // opened but it remains created
}

// only used for testing purposes
int tfs_link_counter(char const *name) {

    inode_t *root_dir_inode = inode_get(ROOT_DIR_INUM);
    ALWAYS_ASSERT(root_dir_inode != NULL, "tfs_open: root dir inode must exist");

    int inum = tfs_lookup(name, root_dir_inode);

    // file doesn't exist, number of hard links = 0
    if (inum==-1) return 0;

    inode_t *inode = inode_get(inum);

    ALWAYS_ASSERT(inode != NULL, "tfs_open: directory files must have an inode");

    int result = (inode->i_links);

    return result;
}

int tfs_sym_link(char const *target, char const *link_name) {
    
    // get the inode from the directory
    inode_t *root_dir_inode = inode_get(ROOT_DIR_INUM);
    ALWAYS_ASSERT(root_dir_inode != NULL, "tfs_sym_link: root dir inode must exist");

    // if creating a symbolic link to a symbolic link: new_target = target of original symbolic link
    // else: new_target = target
    char new_target[MAX_FILE_NAME];
    strcpy(new_target, target);

    // if type of target's inode is T_DIRECTORY then return -1
    int tnum = tfs_lookup(target, root_dir_inode);
    

    if (tnum >= 0) {
        inode_t *tinode = inode_get(tnum);
        // lock the inode
        pthread_rwlock_wrlock(&inode_locks[tnum]);
        ALWAYS_ASSERT(tinode != NULL, "tfs_sym_link: directory files must have an inode");
        
        // creating a symbolic link to a symbolic link
        // creates a separated symbolic link to the file associated with the first symbolic link
        if(tinode->i_node_type==2) {
            // file stored in symbolic link
            char *data = data_block_get(tinode->i_data_block);
            strcpy(new_target, data);
        }
        
        if(tinode->i_node_type == T_DIRECTORY) {
            //unlock the inode
            pthread_rwlock_unlock(&inode_locks[tnum]);
            return -1;
        }
        //unlock the inode
        pthread_rwlock_unlock(&inode_locks[tnum]);
        
    } else { return -1; }

    //create a new inode for the symlink
    int inum = inode_create(T_SYMLINK);
    if (inum == -1) { return -1; }

    inode_t *inode = inode_get(inum);
    // lock the inode
    pthread_rwlock_wrlock(&inode_locks[inum]);

    ALWAYS_ASSERT(inode != NULL, "tfs_sym_link: directory files must have an inode");

    inode->i_size = strlen(new_target);
    inode->i_data_block = data_block_alloc();
    if (inode->i_data_block == -1) {
        //unlock
        pthread_rwlock_unlock(&inode_locks[inum]);
        inode_delete(inum);
        return -1;
    }

    //write the path of target in the data block
    char *data = data_block_get(inode->i_data_block);
    strcpy(data, new_target);

    // add entry in the root directory
    return add_dir_entry(root_dir_inode, link_name + 1, inum);
}

int tfs_link(char const *target, char const *link_name) {
    // get the inode
    inode_t *root_dir_inode = inode_get(ROOT_DIR_INUM);
    ALWAYS_ASSERT(root_dir_inode != NULL, "tfs_link: root dir inode must exist");

    // get the inode of the target
    int inum = tfs_lookup(target, root_dir_inode);
    if (inum == -1) {  return -1; }
    

    inode_t *inode = inode_get(inum);

    // Lock the inode
    pthread_rwlock_wrlock(&inode_locks[inum]);

    ALWAYS_ASSERT(inode != NULL, "tfs_link: directory files must have an inode");

    //check if inode type is T_SYMLINK
    if(inode->i_node_type == T_SYMLINK) { return -1; }

    // increment the link count
    inode->i_links++;

    // Unlock the inode
    pthread_rwlock_unlock(&inode_locks[inum]);
    
    // already returns 0 if successfull, -1 otherwise
    return add_dir_entry(root_dir_inode, link_name + 1, inum);
}

// function that allows user to delete a file or a link
int tfs_unlink(char const *target) {

    inode_t *root_dir_inode = inode_get(ROOT_DIR_INUM);
    ALWAYS_ASSERT(root_dir_inode != NULL, "tfs_unlink: root dir inode must exist");

    //get the inode of the target
    int inum = tfs_lookup(target, root_dir_inode);
    if (inum == -1) { return -1; }
    
    inode_t *inode_to_unlink = inode_get(inum);
    // Lock the inode
    pthread_rwlock_wrlock(&inode_locks[inum]);
    ALWAYS_ASSERT(inode_to_unlink != NULL, "tfs_unlink: directory files must have an inode");

    switch(inode_to_unlink->i_node_type) {

        // symlink
        case(T_SYMLINK):
            inode_delete(inum);
            break;

        // hardlink
        case(T_FILE):
            // check if number of hardlinks reached 0
            if(inode_to_unlink->i_links<=1) {
                if(is_in_open_file_table(inum) != -1) {
                    pthread_rwlock_unlock(&inode_locks[inum]);
                    //error in deleting the inode because the file is open
                    return -1;
                }
                inode_delete(inum);
            }
            else {
                // removes 1 hardlink
                inode_to_unlink->i_links--;
            }
            break;
        
        // trying to unlink something that is not a link
        case(T_DIRECTORY):
            //unlock the inode
            pthread_rwlock_unlock(&inode_locks[inum]);
            return -1;
            break;

        // add default case to avoid compilation error
        default:    
            break;
    }

    // Unlock the inode
    pthread_rwlock_unlock(&inode_locks[inum]);

    // already returns 0 if successfull, -1 otherwise
    return clear_dir_entry(root_dir_inode, target + 1);
}

int tfs_close(int fhandle) {
    open_file_entry_t *file = get_open_file_entry(fhandle);
    if (file == NULL) {
        return -1; // invalid fd
    }

    remove_from_open_file_table(fhandle);

    return 0;
}

ssize_t tfs_write(int fhandle, void const *buffer, size_t to_write) {
    open_file_entry_t *file = get_open_file_entry(fhandle);
    if (file == NULL) {
        return -1;
    }

    //  From the open file table entry, we get the inode
    inode_t *inode = inode_get(file->of_inumber);

    // Lock the inode
    pthread_rwlock_wrlock(&inode_locks[file->of_inumber]);

    ALWAYS_ASSERT(inode != NULL, "tfs_write: inode of open file deleted");

    // Determine how many bytes to write
    //size_t block_size = state_block_size();
    //if (to_write + file->of_offset > block_size) {
    //    to_write = block_size - file->of_offset;
    //}

    printf("tfs_write: writing %zu bytes at offset %zu\n", to_write, file->of_offset);

    if (to_write > 0) {
        if (inode->i_size == 0) {
            // If empty file, allocate new block
            int bnum = data_block_alloc();
            if (bnum == -1) {
                // Unlock the inode
                pthread_rwlock_unlock(&inode_locks[file->of_inumber]);
                return -1; // no space
            }

            inode->i_data_block = bnum;
        }

        void *block = data_block_get(inode->i_data_block);
        

        ALWAYS_ASSERT(block != NULL, "tfs_write: data block deleted mid-write");

        // Perform the actual write
        memcpy(block + file->of_offset, buffer, to_write);

        // The offset associated with the file handle is incremented accordingly
        file->of_offset += to_write;
        if (file->of_offset > inode->i_size) {
            inode->i_size = file->of_offset;
        }

        printf("tfs_write: wrote %zu new offset %zu\n", to_write, file->of_offset);
    }

    // Unlock the inode
    pthread_rwlock_unlock(&inode_locks[file->of_inumber]);

    return (ssize_t)to_write;
}

ssize_t tfs_read(int fhandle, void *buffer, size_t len) {
    open_file_entry_t *file = get_open_file_entry(fhandle);
    if (file == NULL) {
        return -1;
    }

    // From the open file table entry, we get the inode
    inode_t *inode = inode_get(file->of_inumber);
    ALWAYS_ASSERT(inode != NULL, "tfs_read: inode of open file deleted");
    
    // Lock the inode
    pthread_rwlock_rdlock(&inode_locks[file->of_inumber]);
    
    size_t to_read = inode->i_size - file->of_offset;

    printf("tfs_read: inode size: %zd, file offset: %zd, to_read: %zd\n", inode->i_size, file->of_offset, to_read);

    if (to_read > len) {
        to_read = len;
    }

    if (to_read > 0) {
        void *block = data_block_get(inode->i_data_block);

        ALWAYS_ASSERT(block != NULL, "tfs_read: data block deleted mid-read");

        // Perform the actual read
        memcpy(buffer, block + file->of_offset, to_read);
        // The offset associated with the file handle is incremented accordingly
        file->of_offset += to_read;
    }  

    // Unlock the inode
    pthread_rwlock_unlock(&inode_locks[file->of_inumber]);

    return (ssize_t)to_read;
}

int tfs_rewind(int fhandle) {
    open_file_entry_t *file = get_open_file_entry(fhandle);
    if (file == NULL) {
        return -1;
    }

    file->of_last_offset = file->of_offset;
    file->of_offset = 0;

    return 0;
}

int tfs_seek(int fhandle) {
    open_file_entry_t *file = get_open_file_entry(fhandle);
    if (file == NULL) {
        return -1;
    }

    if(file->of_offset > file->of_last_offset)
        return 0;
    else
        file->of_offset = file->of_last_offset;

    return 0;
}

int tfs_copy_from_external_fs(char const *source_path, char const *dest_path) {
    
    FILE* source = fopen(source_path, "r");
    
    int dest = tfs_open(dest_path, TFS_O_CREAT | TFS_O_TRUNC | TFS_O_APPEND);

    if (source == NULL || dest == -1) { return -1; }

    fseek(source, 0L, SEEK_END);    // move file pointer until end of file
    size_t size = (size_t)ftell(source);      // gets size of file

    char buffer[size];              // creates buffer with size of file
    memset(buffer,0,size);          // clears memory (not needed since everything
                                    // is getting overwritten) with standard x size
			                        // needs because file length is unknown.

    /* read the contents of the file */
    rewind(source);                  // bring file pointer to the beginning so it 
			                        // can be read, (moved in fseek())
    ssize_t bytes_read = (ssize_t)fread(buffer, 1, size, source);
    if (bytes_read < 0) { return -1; }
   
    ssize_t bytes_written = tfs_write(dest, buffer, size);
    if (bytes_written < 0) { return -1; }

    fclose(source);
    tfs_close(dest);

    return 0;
}