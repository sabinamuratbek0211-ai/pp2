CREATE OR REPLACE PROCEDURE upsert_contact(
    p_username VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE username = p_username) THEN
        UPDATE phonebook SET phone = p_phone WHERE username = p_username;
    ELSE
        INSERT INTO phonebook(username, phone)
        VALUES (p_username, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(
    p_username VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_username IS NOT NULL THEN
        DELETE FROM phonebook WHERE username = p_username;
    ELSIF p_phone IS NOT NULL THEN
        DELETE FROM phonebook WHERE phone = p_phone;
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_usernames TEXT[],
    p_phones TEXT[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_usernames, 1) LOOP
        IF p_phones[i] ~ '^\+?[0-9]{10,15}$' THEN
            IF EXISTS (SELECT 1 FROM phonebook WHERE username = p_usernames[i]) THEN
                UPDATE phonebook SET phone = p_phones[i]
                WHERE username = p_usernames[i];
            ELSE
                INSERT INTO phonebook(username, phone)
                VALUES (p_usernames[i], p_phones[i]);
            END IF;
        END IF;
    END LOOP;
END;
$$;