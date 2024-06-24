DO $$
DECLARE
    rec RECORD;
    year INTEGER;
    roi NUMERIC;
BEGIN
	 -- Create temporary table for unique tickers
    CREATE TEMP TABLE unique_tickers AS
    SELECT DISTINCT ticker
    FROM stock_data;

    -- Loop through each unique ticker
    FOR rec IN (SELECT ticker FROM unique_tickers) LOOP
        -- Loop through each year from 2010 to 2024
        FOR year IN 2010..2024 LOOP
            roi := calculate_roi(rec.ticker, year);

            -- Update or insert the stock_returns table
            UPDATE stock_returns
            SET
                return_2024 = CASE WHEN year = 2024 THEN roi ELSE return_2024 END,
                return_2023 = CASE WHEN year = 2023 THEN roi ELSE return_2023 END,
                return_2022 = CASE WHEN year = 2022 THEN roi ELSE return_2022 END,
                return_2021 = CASE WHEN year = 2021 THEN roi ELSE return_2021 END,
                return_2020 = CASE WHEN year = 2020 THEN roi ELSE return_2020 END,
                return_2019 = CASE WHEN year = 2019 THEN roi ELSE return_2019 END,
                return_2018 = CASE WHEN year = 2018 THEN roi ELSE return_2018 END,
                return_2017 = CASE WHEN year = 2017 THEN roi ELSE return_2017 END,
                return_2016 = CASE WHEN year = 2016 THEN roi ELSE return_2016 END,
                return_2015 = CASE WHEN year = 2015 THEN roi ELSE return_2015 END,
                return_2014 = CASE WHEN year = 2014 THEN roi ELSE return_2014 END,
                return_2013 = CASE WHEN year = 2013 THEN roi ELSE return_2013 END,
                return_2012 = CASE WHEN year = 2012 THEN roi ELSE return_2012 END,
                return_2011 = CASE WHEN year = 2011 THEN roi ELSE return_2011 END,
                return_2010 = CASE WHEN year = 2010 THEN roi ELSE return_2010 END
            WHERE ticker = rec.ticker;

            -- If no rows were updated, insert a new row
            IF NOT FOUND THEN
                INSERT INTO stock_returns (ticker, return_2024, return_2023, return_2022, return_2021, return_2020, return_2019, return_2018, return_2017, return_2016, return_2015, return_2014, return_2013, return_2012, return_2011, return_2010)
                VALUES (rec.ticker, 
                        CASE WHEN year = 2024 THEN roi ELSE NULL END,
                        CASE WHEN year = 2023 THEN roi ELSE NULL END,
                        CASE WHEN year = 2022 THEN roi ELSE NULL END,
                        CASE WHEN year = 2021 THEN roi ELSE NULL END,
                        CASE WHEN year = 2020 THEN roi ELSE NULL END,
                        CASE WHEN year = 2019 THEN roi ELSE NULL END,
                        CASE WHEN year = 2018 THEN roi ELSE NULL END,
                        CASE WHEN year = 2017 THEN roi ELSE NULL END,
                        CASE WHEN year = 2016 THEN roi ELSE NULL END,
                        CASE WHEN year = 2015 THEN roi ELSE NULL END,
                        CASE WHEN year = 2014 THEN roi ELSE NULL END,
                        CASE WHEN year = 2013 THEN roi ELSE NULL END,
                        CASE WHEN year = 2012 THEN roi ELSE NULL END,
                        CASE WHEN year = 2011 THEN roi ELSE NULL END,
                        CASE WHEN year = 2010 THEN roi ELSE NULL END);
            END IF;
        END LOOP;
    END LOOP;
END;
$$;
