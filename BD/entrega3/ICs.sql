 -- (RI-1) Nenhum empregado pode ter menos de 18 anos de idade.

CREATE OR REPLACE FUNCTION validate_age()
RETURNS TRIGGER AS 
$$
BEGIN
    DELETE FROM employee
    WHERE ssn = NEW.ssn
    AND NEW.bdate > (CURRENT_DATE - INTERVAL '18 years');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tg_validate_age ON employee CASCADE;
CREATE TRIGGER tg_validate_age
AFTER INSERT ON employee
FOR EACH ROW EXECUTE PROCEDURE validate_age();


 -- (RI-2) Um 'Workplace' é obrigatoriamente um 'Office' ou 'Warehouse' mas não pode ser ambos
 -- 'Workplace' ser 'Office' e 'Warehouse' impossibilitado por "PRIMARY KEY (address)" em 'Office' e 'Warehouse'

CREATE OR REPLACE FUNCTION validate_workplace()
RETURNS TRIGGER AS
$$
BEGIN
    DELETE FROM workplace
    WHERE address = NEW.address
    AND ( address NOT IN ( (SELECT address FROM office) UNION (SELECT address FROM warehouse) ) OR
          address IN ( (SELECT address FROM office) INTERSECT (SELECT address FROM warehouse) ) );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tg_validate_workplace ON workplace CASCADE;
CREATE CONSTRAINT TRIGGER tg_validate_workplace
AFTER INSERT ON workplace DEFERRABLE
FOR EACH ROW EXECUTE PROCEDURE validate_workplace();


 -- (RI-3) Uma 'Order' tem de figurar obrigatoriamente em 'Contains'.

CREATE OR REPLACE FUNCTION validate_order()
RETURNS TRIGGER AS
$$
BEGIN
    DELETE FROM order_
    WHERE order_no = NEW.order_no
    AND NEW.order_no NOT IN (SELECT order_no FROM contains);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tg_validate_order ON order_ CASCADE;
CREATE CONSTRAINT TRIGGER tg_validate_order
AFTER INSERT ON order_ DEFERRABLE
FOR EACH ROW EXECUTE PROCEDURE validate_order();