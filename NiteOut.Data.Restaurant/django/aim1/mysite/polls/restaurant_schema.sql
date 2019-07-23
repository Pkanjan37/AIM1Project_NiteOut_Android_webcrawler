CREATE TABLE Cuisine
( 
	cuisineType          varchar(100)  NULL ,
	restaurantID         varchar(100)  NULL 
);




CREATE TABLE Location
( 
	locationID           varchar(100)  NULL ,
	address              varchar  NULL ,
	longitude            float  NULL ,
	latitude             float  NULL 
);




CREATE TABLE Photo
( 
	photoID              serial primary key ,
	pictureURL           varchar  NULL ,
	restaurantID         varchar(100)  NULL 
);




CREATE TABLE Restaurant
( 
	restaurantID         varchar(100)  NULL  ,
	priceRange           varchar(100)  NULL ,
	website              text  NULL ,
	phoneNumber          varchar(100)  NULL ,
	locationID           varchar(100)  NULL 
);




CREATE TABLE RestaurantFeature
( 
	featureName          text  NULL ,
	restaurantID         varchar(100)  NULL ,
	description          text  NULL 
);




CREATE TABLE RestaurantRating
( 
	ratingID             serial primary key ,
	scale                varchar(100)  NULL ,
	overallRating        float  NULL ,
	source               varchar(100)  NULL ,
	restaurantID         varchar(100)  NULL 
);





CREATE TABLE UserReview
( 
	reviewID             serial primary key ,
	comment              text  NULL ,
	reviewRating         float  NULL ,
	reviewDate           timestamp default  NULL ,
	restaurantID         varchar(100)  NULL 
);
