/** @odoo-module **/

import {registry} from "@web/core/registry";
import {Component, onWillStart} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import { useRef, onPatched, onMounted, useState } from "@odoo/owl";
const actionRegistry = registry.category("actions");

export class DashboardFleetRental extends Component {
    async setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            top_customers: [],
            available_vehicle_details: {},
            available_cars: false,
            running_cars: {},
            running_vehicle_details: {},
        });
        this.modal_warning = useRef("modal_warning");
        this.most_rented_cars_bar = useRef("most_rented_cars_bar");
        this.start_date = useRef("start_date");
        this.end_date = useRef("end_date");

        onWillStart(async () => {
            this.props.title = 'Dashboard';
            await this.fetch_data();
        });

        onMounted(async () => {
            await this.render_graphs();
        });
    }

    async fetch_data() {
        var self = this;
        await this.orm.call("car.rental.contract", "cars_availability", []).then(function(data) {
            self.state.available_cars = data['available_cars'];
            self.state.running_cars = data['cars_running'];
        });
        await this.orm.call("car.rental.contract", "car_details", []).then(function(data) {
            self.state.running_vehicle_details = data['running_details'];
            self.state.available_vehicle_details = data['available_cars'];
        });
        await this.orm.call("car.rental.contract", "top_customers", []).then(function(data) {
            self.state.top_customers = data;
        });
    }

    render_graphs(){
        this.render_most_rented_cars_bar();
    }

    render_most_rented_cars_bar() {
        var self = this;

        if (this.chartStatus) {
            if (this.chartStatus.bar) {
                this.chartStatus.bar.destroy();
            }
        }

        this.orm.call('car.rental.contract', 'vehicle_most_rented', [this.start_date.el.value, this.end_date.el.value]).then(result => {
            const colors = ["red", "blue", "green", "orange", "purple", "steel", "rebecca", "brown", "pink", "grey", "black"];
            var ctx = self.most_rented_cars_bar.el;
            var name = result.name.slice(0, 5); // Top 5 cars
            var count = result.num.slice(0, 5); // Top 5 counts

            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: name,
                    datasets: [{
                        label: 'Count',
                        data: count,
                        backgroundColor: colors,
                        borderColor: colors,
                        barPercentage: 0.5,
                        barThickness: 100,
                        maxBarThickness: 100,
                        minBarLength: 0,
                        borderWidth: 1,
                        fill: false
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        },
                    },
                    responsive: true,
                    maintainAspectRatio: false,
                }
            });

            this.chartStatus = {
                bar: myChart
            };

        }).catch(error => {
            console.error('Error rendering chart:', error);
        });
    }

    onApplyFilter() {
        if (this.start_date.el.value && this.end_date.el.value) {
            if (this.start_date.el.value > this.end_date.el.value) {
                this.modal_warning.el.style.display = "block";
                return false;
            }
        }
        this.render_graphs();
    }

    closeModal() {
        this.modal_warning.el.style.display = "none";
    }
}

DashboardFleetRental.template = "CustomDashBoard";
actionRegistry.add("fleet_rental_dashboard", DashboardFleetRental);
