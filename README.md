# Entity Relationship Diagram

----
![Entity Relationship Diagram](https://i.imgur.com/rcottlD.png)

---
### Preface

Additional changes are suggested here, such as adding a default generated column on bookings to calculate the total price with overriding functionality - as some customers may get discounts and so on, or adding a column to the bookings table to store the date the booking was made. The former is often generated with ORMs.

In addition, the tests provided in this demonstration only cover basic functionality, such as the creation, fetching, and deletion of existing entites. This should be extended to updated, and then extended to the reporting functionality.

No ORM was used, however, I built a little dataclass helper to make it easier to create and manipulate the entities, if you look over models.base.py, the helper is the only class there called `BaseModel`, with the update, get, create and delete functionalities attached.

Another note to make is that hash is never exposed to the frontend, as it is used to authenticate the user, this little functionality was added to the BaseModel, allowing further usage of it in other classes. Overall, the abstraction is incredibly helpful, and without it, there would have been very static and unreadable code.

### Deployment
Fargate over Docker seems to be the most rudimentary and scalable method to this application. There may be use of S3 for contracts signed between the customers & the rental shop, and perhaps usage of SES or other mailing services is implied through the confirmation letter (which can be transformed to a confirmation e-mail, much cheaper and faster).

---

# SQL (DDL)

---

```sql
create table categories
(
	id int auto_increment,
	name varchar(50) not null,
	carry_capacity int not null,
	constraint categories_id_uindex
		unique (id)
)
comment 'Contains the different vehicle categories';

alter table categories
	add primary key (id);

create table customers
(
	id int auto_increment
		primary key,
	name varchar(100) not null,
	number varchar(14) not null,
	email varchar(50) null comment 'It is presumed either an email or an address is required for the confirmation letter',
	address varchar(95) null,
	hash char(128) null comment 'An application like this should probably have a web interface, meaning that the customers are probably expected to have accounts',
	constraint customers_email_uindex
		unique (email)
)
comment 'The various customers of the rental agency';

create table vehicles
(
	id int auto_increment,
	name varchar(50) not null,
	category_id int null,
	price_per_day decimal(10,3) not null comment 'Very important to set this as decimal rather than float or double, since this is monetary',
	constraint vehicles_id_uindex
		unique (id),
	constraint vehicles_categories_id_fk
		foreign key (category_id) references categories (id)
			on update cascade
)
comment 'The different rentable vehicles';

alter table vehicles
	add primary key (id);

create table bookings
(
	id int auto_increment
		primary key,
	vehicle_id int not null,
	customer_id int not null,
	hire_date datetime not null comment 'Using datetime instead of date is an interesting concept, as it should technically allow the rental service to be more efficient, and perhaps rake in more deliveries',
	end_date datetime not null,
	confirmed tinyint(1) default 0 not null,
	constraint bookings_customers_id_fk
		foreign key (customer_id) references customers (id)
			on update cascade,
	constraint bookings_vehicles_id_fk
		foreign key (vehicle_id) references vehicles (id)
			on update cascade
)
comment 'The various bookings held by customers';

create index bookings_hire_date_end_date_confirmed_index
	on bookings (hire_date, end_date, confirmed);


```

The above SQL is the DDL SQL for the database, which is used to create the database. I have been very sparse with index creation, the only index that comes to note that isn't immediately obvious is the one on the bookings table, which is created to allow for the efficient fetching of bookings based on the hire date, end date and confirmed status.

As the data grows, the only table that comes to mind that might have an exponential growth is bookings, especially since:
1. Historical data is necessary.
2. The number of bookings is expected to be very high, with unconfirmed bookings being the most notable.

Currently, all the interactions with the database run over indexed queries.
Another thing to note is all deletions are restricted, with all updates are set to cascade. It makes no sense to delete a vehicle that has history of bookings. Presuming this is a live environment, I would recommend soft deletion, as vehicles are bound to deprecate, but historical data should be maintained and a dump to an analytic database may be necessary every three months (this is a guess based on this specific market's activities - which I don't imagine are very volatile).