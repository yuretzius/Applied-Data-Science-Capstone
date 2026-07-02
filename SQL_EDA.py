#### this only works in jupyter notebook

%load_ext sql

import csv, sqlite3
import prettytable
prettytable.DEFAULT = 'DEFAULT'

con = sqlite3.connect("my_data1.db")
cur = con.cursor()

%sql sqlite:///my_data1.db

import pandas as pd
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")

#DROP THE TABLE IF EXISTS

%sql DROP TABLE IF EXISTS SPACEXTABLE;

%sql create table SPACEXTABLE as select * from SPACEXTBL where Date is not null

# Tasks

# Now write and execute SQL queries to solve the assignment tasks.

# Note: If the column names are in mixed case enclose it in double quotes For Example "Landing_Outcome"

# Task 1
# Display the names of the unique launch sites in the space mission

%sql SELECT DISTINCT LAUNCH_SITE as "Launch_Sites" FROM SPACEXTBL;

# Launch_Sites
# CCAFS LC-40
# VAFB SLC-4E
# KSC LC-39A
# CCAFS SLC-40

# Task 2
# Display 5 records where launch sites begin with the string 'CCA'

%sql SELECT * FROM 'SPACEXTBL' WHERE Launch_Site LIKE 'CCA%' LIMIT 5;

# CCAFS LC-40
# CCAFS LC-40
# CCAFS LC-40
# CCAFS LC-40
# CCAFS LC-40

# Task 3
# Display the total payload mass carried by boosters launched by NASA (CRS)

%sql SELECT SUM(PAYLOAD_MASS__KG_) as "Total Payload Mass(Kgs)", Customer FROM 'SPACEXTBL' WHERE Customer = 'NASA (CRS)';

# Total Payload Mass(Kgs) 	Customer
                 # 45596   	NASA (CRS)

# Task 4
# Display average payload mass carried by booster version F9 v1.1

%sql SELECT AVG(PAYLOAD_MASS__KG_) as "Payload Mass Kgs", Customer, Booster_Version FROM 'SPACEXTBL' WHERE Booster_Version LIKE 'F9 v1.1';

# Payload Mass Kgs 	Customer 	Booster_Version
        # 2928.4      	SES 	F9 v1.1

# Task 5
# List the date when the first succesful landing outcome in ground pad was acheived.

# Hint:Use min function 

%sql SELECT MIN(DATE) FROM 'SPACEXTBL' WHERE "Landing_Outcome" = "Success (ground pad)";

# MIN(DATE)
# 2015-12-22

%sql SELECT DISTINCT "Landing_Outcome" FROM SPACEXTBL;

# Landing_Outcome
# Failure (parachute)
# No attempt
# Uncontrolled (ocean)
# Controlled (ocean)
# Failure (drone ship)
# Precluded (drone ship)
# Success (ground pad)
# Success (drone ship)
# Success
# Failure
# No attempt 

# Task 6
# List the names of the boosters which have success in drone ship and have payload mass greater than 4000 but less than 6000

%sql SELECT DISTINCT Booster_Version, Payload FROM SPACEXTBL WHERE "Landing_Outcome" = "Success (drone ship)" AND PAYLOAD_MASS__KG_ < 6000 AND PAYLOAD_MASS__KG_ > 4000;

# Booster_Version 	Payload
# F9 FT B1022 	JCSAT-14
# F9 FT B1026 	JCSAT-16
# F9 FT B1021.2 	SES-10
# F9 FT B1031.2 	SES-11 / EchoStar 105

# Task 7
# List the total number of successful and failure mission outcomes

%sql SELECT "Mission_Outcome", COUNT("Mission_Outcome") as Total FROM SPACEXTBL GROUP BY "Mission_Outcome";

# Mission_Outcome                	Total
# Failure (in flight)            	1
# Success 	                        98
# Success 	                        1
# Success (payload status unclear) 	1

# Task 8
# List all the booster_versions that have carried the maximum payload mass, using a subquery with a suitable aggregate function.

%sql SELECT "Booster_Version",Payload, "PAYLOAD_MASS__KG_" FROM SPACEXTBL WHERE "PAYLOAD_MASS__KG_" = (SELECT MAX("PAYLOAD_MASS__KG_") FROM SPACEXTBL);

# Booster_Version 	Payload 	PAYLOAD_MASS__KG_
# F9 B5 B1048.4 	Starlink 1 v1.0, SpaceX CRS-19 	15600
# F9 B5 B1049.4 	Starlink 2 v1.0, Crew Dragon in-flight abort test 	15600
# F9 B5 B1051.3 	Starlink 3 v1.0, Starlink 4 v1.0 	15600
# F9 B5 B1056.4 	Starlink 4 v1.0, SpaceX CRS-20 	15600
# F9 B5 B1048.5 	Starlink 5 v1.0, Starlink 6 v1.0 	15600
# F9 B5 B1051.4 	Starlink 6 v1.0, Crew Dragon Demo-2 	15600
# F9 B5 B1049.5 	Starlink 7 v1.0, Starlink 8 v1.0 	15600
# F9 B5 B1060.2 	Starlink 11 v1.0, Starlink 12 v1.0 	15600
# F9 B5 B1058.3 	Starlink 12 v1.0, Starlink 13 v1.0 	15600
# F9 B5 B1051.6 	Starlink 13 v1.0, Starlink 14 v1.0 	15600
# F9 B5 B1060.3 	Starlink 14 v1.0, GPS III-04 	15600
# F9 B5 B1049.7 	Starlink 15 v1.0, SpaceX CRS-21 	15600

# Task 9
# List the records which will display the month names, failure landing_outcomes in drone ship ,booster versions, launch_site for the months in year 2015.

# Note: SQLLite does not support monthnames. So you need to use substr(Date, 6,2) as month to get the months and substr(Date,0,5)='2015' for year.

%sql SELECT substr(Date,6,2) as "Month", substr(Date,0,5) as "Year","Booster_Version", "Launch_Site", Payload, "PAYLOAD_MASS__KG_", "Mission_Outcome", "Landing_Outcome" FROM SPACEXTBL WHERE substr(Date,0,5)='2015' AND "Landing_Outcome" = 'Failure (drone ship)';

# Month 	Year 	Booster_Version 	Launch_Site 	Payload 	    PAYLOAD_MASS__KG_ 	Mission_Outcome 	Landing_Outcome
# 01 	    2015 	F9 v1.1 B1012 	    CCAFS LC-40 	SpaceX CRS-5 	2395 	            Success         	Failure (drone ship)
# 04    	2015 	F9 v1.1 B1015   	CCAFS LC-40 	SpaceX CRS-6 	1898 	            Success 	        Failure (drone ship)


# Task 10
# Rank the count of landing outcomes (such as Failure (drone ship) or Success (ground pad)) between the date 2010-06-04 and 2017-03-20, in descending order.

%sql SELECT "Landing_Outcome", COUNT("Landing_Outcome") as Total FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY "Landing_Outcome" ORDER BY Total DESC;

# Landing_Outcome 	        Total
# No attempt 	            10
# Success (drone ship)  	5
# Failure (drone ship)  	5
# Success (ground pad)  	3
# Controlled (ocean) 	    3
# Uncontrolled (ocean)  	2
# Failure (parachute) 	    2
# Precluded (drone ship) 	1
