# Data Engineer Tech Challenge (Answer Edition)

## Section 1: Data Pipelines

### Processed Dataset : 
Found in the folders `reject_dataset` and `success_dataset`
### Scripts: `process_dataset.py`

---

## Section 2: Databases

### Docker container build:
 `posttgres.yml`
### DDL Statement: 
`table_ddl\creation_tables`
### Entity-Relationship diagrams: 
![alt text](https://github.com/paulwija-work/DETechAssessment-23/blob/main/postgres_tables.png?raw=true)

### SQL Questions
```
1. Which are the top 10 members by spending

select  customer_id , sum(revenue) as total_revenue
from sales
group by customer_id
ORDER BY total_revenue desc
limit 10

2. Which are the top 3 items that are frequently brought by members

select  product_id , sum(quantity) as total_quantity
from sales
group by product_id
ORDER BY total_quantity desc
limit 3

```

---

## Section 3: System Design
### Assumption:

```
- A scheduler has been set up in the cloud environment to purge images and its metadata that exceed 7 days mark
- There should not be a need to purge the data gotten from processing the images as it should already be hashed to retain privacy for the users while preventing duplicated images data to be inserted to the database
- cloud computing can be a small scale opertaion as the database should be stored in a RDS and a load balancer has already been created to control the traffic of the api in order to not overload the system.
```

### End-to-End flow : 
![alt text](https://github.com/paulwija-work/DETechAssessment-23/blob/main/System%20Design.png?raw=true)


---
## Section 4: Charts & APIs

### Issue:
Data cannot be found as the API is not longer accessible and also inexperience in API
---


## Section 5: Machine Learning

### Issue:
Inexperience in Machine Learning