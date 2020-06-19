# ERA5 Display App

## A mere GUI to display data from the Copernicus Climate Data Store

The goal of such an app is to make it easier for people to look at ERA5 data.
With this GUI, the user just have to download data from the ***[Copernicus Climate Data Store (CDS)](https://cds.climate.copernicus.eu/#!/home)***.

---

*The whole script is currently under development.*

## Introduction

*To do*

## Requirements

*To do*

### Basemap

## Setup

*To do*

## How to download data

This part is for non-regular users.   
At the moment, you might wonder:

> Ok, now my installation is complete. But how do I get some data?

Well, you mainly have two possibilities: get them manually from the CDS or use the python module `cdsapi`. ***In both cases, make sure you're downloading data in netCDF format (.nc files).***

### Retrieve data from CDS

First, you need to sign up and create an account (I guess you don't have an account yet if you're reading this). Once you're logged in, look at the top left corner of your window, and go to the datasets section.

![Datasets section](/ressources/images/cds_1.PNG "First look at CDS")

This will open a browser. A bunch of datasets are available, as you can see. But don't worry, we won't dive into the depths of the CDS.  
Type *ERA5* in the search bar to shorten datasets list. We'll focus on (only) 6 datasets:

- *ERA5 hourly data on single levels from 1979 to present*
- *ERA5 hourly data on pressure levels from 1979 to present*
- *ERA5 monthly averaged data on single levels from 1979 to present*
- *ERA5 monthly averaged data on pressure levels from 1979 to present*
- *ERA5-Land hourly data on single levels from 1981 to present*
- *ERA5-Land monthly averaged data on single levels from 1981 to present*

Choose a dataset. You should get something like this:

![Opening a dataset](/ressources/images/cds_2.PNG "Opening a dataset")

In the *Overview* tab, you'll get basic information on the dataset itself, its variables etc... In the *Download Data* tab, you'll be able to choose the variables you want to look at, the time period, the AOI and so on.

**Don't forget at the end to check the data format!**

![Data format](/ressources/images/cds_3.PNG )

### Retrieve data with Python

You can also use Python to retrieve you're data in an efficient way.  
You'll need to install `cdsapi` at first. A pip install command in your terminal should be fine:

```
pip install cdsapi
or
python -m pip install cdsapi
```

As I'm not a proficient user of `cdsapi`, I'll let you check ***[how to complete the installation by yourself](https://cds.climate.copernicus.eu/api-how-to)***.

