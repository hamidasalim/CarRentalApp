export const Causes = {
  getCausesData() {
    return [
      {
        id: 1,
        title: "Competitive Tunisia Car Rent Price",
        desc: "Rent a car in Tunisia at affordable and competitive prices. Save money with hourly, daily, weekly or monthly rent options",
        icon: "serviceIcon.svg",
        bgIcon: "#5B72EE",
      },
      {
        id: 2,
        title: "Friendly Service",
        desc: "Hamida's Car Rent always prioritizes friendly service for your comfort and smooth travel.",
        icon: "carIcon.svg",
        bgIcon: "#F48C06",
      },
      {
        id: 3,
        title: "Newest Car Fleet",
        desc: "Hamida's Car rentals provides the latest fleet of cars with regular maintenance for the perfect travel experience.",
        icon: "moneyIcon.svg",
        bgIcon: "#29B9E7",
      },
      {
        id: 5,
        title: "Car Rent  self drive",
        desc: "Enjoy privacy and comfort with Hamida's Car Rentals off-key car rental service. Terms and conditions apply.",
        icon: "keyIcon.svg",
        bgIcon: "#F48C06",
      },
      {
        id: 6,
        title: "Shuttle Service",
        desc: "Take advantage of Hamida's Car rentals Tunisia's shuttle service to/from the airport, terminal, hotels, and other locations in Tunisia",
        icon: "betweenIcon.svg",
        bgIcon: "#5eead4",
      },
    ];
  },
  getCauses() {
    return Promise.resolve(this.getCausesData());
  },
};
