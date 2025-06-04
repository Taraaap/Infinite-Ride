// navbar
const navLinks = document.querySelectorAll('#navbar a');
const currentUrl = window.location.pathname;
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentUrl) {
        link.classList.add('active');
    }
});



//model vehicle
const vehicleDetailsButtons = document.querySelectorAll('.details[data-bs-target="#vehicle-modal"]');

// Loop through each button and add an event listener
vehicleDetailsButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Fetching the data attributes for each vehicle inside the click event
        const vehicleName = button.getAttribute('data-vehicle-name');
        const vehicleDescription = button.getAttribute('data-vehicle-des');
        const vehiclePrice = button.getAttribute('data-vehicle-price');
        const vehicleImage = button.getAttribute('data-vehicle-image');
        const vehicleSeatingCapacity = button.getAttribute('data-vehicle-seating-capacity');
        const fuelType = button.getAttribute('data-vehicle-fuel-type');
        const transmissionType = button.getAttribute('data-vehicle-transmission-type');
        const engineCapacity = button.getAttribute('data-vehicle-engine-capacity');
        const needsDriver = button.getAttribute('data-vehicle-driver-required') === 'True' ? 'Yes' : 'No';

        // Populate the modal with the vehicle data
        document.getElementById('vehicle-name').textContent = vehicleName;
        document.getElementById('vehicle-des').textContent = vehicleDescription;
        document.getElementById('vehicle-price').textContent = `Rs${vehiclePrice}/day`;
        document.getElementById('vehicle-image').src = vehicleImage;

        // Populate extra details with proper HTML formatting
        document.getElementById('fuel-type-placeholder').innerHTML = fuelType ? `<strong>Fuel Type:</strong> ${fuelType}` : '';
        document.getElementById('transmission-type-placeholder').innerHTML = transmissionType ? `<strong>Transmission Type:</strong> ${transmissionType}` : '';
        document.getElementById('engine-capacity-placeholder').innerHTML = engineCapacity ? `<strong>Engine Capacity:</strong> ${engineCapacity}` : '';
        document.getElementById('seating-capacity-placeholder').innerHTML = vehicleSeatingCapacity ? `<strong>Seating Capacity:</strong> ${vehicleSeatingCapacity}` : '';
        });
});




    // Event listener for when a "Book Now" button is clicked
    const bookNowButtons = document.querySelectorAll('.book-now');

    bookNowButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Get the vehicle details from the clicked button's data attributes
            const vehicleName = button.getAttribute('data-vehicle-name');
            const vehiclePrice = button.getAttribute('data-vehicle-price');
            const vehicleId = button.getAttribute('data-vehicle-id');
            
            // Set the vehicle name and price in the modal
            document.getElementById('vehicle-id').value = vehicleId;
            document.getElementById('booking-price').value = "Rs" + vehiclePrice + "/day";

            // You can set the vehicle name in the modal if you want to display it too
            // For example, you might show it in the booking form (optional)
            // document.getElementById('vehicle-name-display').innerText = vehicleName;
        });
    });




// login

    