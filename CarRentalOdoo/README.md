# Fleet Rental Management System - README

## Project Overview

This repository contains a comprehensive **Odoo 17-based Fleet Rental Management System** with two integrated modules designed for managing car rental operations and analytics.

## Modules

* **fleet_rental**

  * Core rental management module handling:

     Vehicles
     Contracts
     Payments

* **fleet_rental_dashboard**

  * Analytics and visualization module providing insights into:

     Vehicle usage
     Rentals
     Customer data

## Architecture

* **Models**: Business logic implemented using **Odoo ORM**.
* **Views**: XML-based UI including **Kanban, Form, and Tree views**.
* **Controllers**: JSON-RPC endpoints for frontend integration.
* **Security**: Role-based access control with **groups** and **record rules**.

## Key Features

* **Car Rental Contracts**

   Workflow states: draft → reserved → running → done/cancel.

* **Maintenance Alerts**

  * Tracks deadlines for:

     Oil change
     Insurance
     Leasing
     Technical inspection
     Road tax

* **Payment and Invoicing**

   Handle payments and tax calculations
   Generate invoices
   Update contract status

* **Vehicle Availability Logic**

   Prevents double-booking using **dynamic domain filtering**.

* **Dashboard Analytics**

   Vehicle availability
   Most rented cars
   Top customers

* **Email Notifications**

  * Scheduled reminders for:

     Contract expirations
     Maintenance deadlines

* **Multi-company Support**

   Users see only records relevant to their company.

## Technical Highlights

* **Model Inheritance**: Extends core Odoo models like:

   fleet.vehicle
   account.payment
   account.move
   res.users

* **Computed Fields**: Dynamic calculations for:

   Total cost
   Rental duration
   Extra charges
   Fuel rates

* **API Integration**: JSON-RPC endpoints for external systems and frontend communication.

* **Frontend Technologies**:

   OWL framework
   JavaScript ES6+
   Chart.js for dashboards
   Responsive UI with SCSS and Bootstrap

* **Security**:

   Role-based access
   Field-level permissions
   Safe admin operations using sudo()

* **Database**: PostgreSQL, optimized for performance and indexing.

## Configuration and Customization

 Contract reminder days
 Tax and stamp rates
 Alert thresholds for maintenance types
 Email templates for automated notifications
 Extensible to add:

  - New vehicle fields
  - Maintenance types
  - Custom reports

## Database Schema Highlights

* **car.rental.contract**: Links customer, vehicles, payments, and checklists
* **fleet.vehicle**: Tracks driver and rental reservation details
* **account.payment**: Associated with contracts and customers for payment tracking
* **Other models**:

   EmployeeFleet
   FleetUser
   Contract lines
   Reserved vehicles
   Tools
   Settings
   Partner data

## Getting Started

1-Clone the repository.
2-Install dependencies as per Odoo 17 documentation.
3-Load modules fleet_rental and fleet_rental_dashboard in your Odoo instance.
4-Start managing fleet rentals and monitoring analytics.
