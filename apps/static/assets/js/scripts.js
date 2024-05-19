const ToastLevel = {
    Info: "black",
    Success: "green",
    Warning: "orange",
    Error: "red"
}

function formatNumber(value) {
    value = parseFloat(value.replace(/[^\d.-]/g, ''));
    return new Intl.NumberFormat('de-DE', {style: 'currency', currency: 'EUR', minimumFractionDigits: 0}).format(value);
}

function unformatNumber(value) {
    value = value.replace(/\s*€\s*/g, '');
    value = value.replace(',', '.');
    value = value.replace(/\.\d{3}/g, match => match.replace('.', ''));
    return value;
}

function cleanPrice(price) {
    return price.replace(/[€, ]/g, '');
}

function parseDate(dateStr) {
    const parts = dateStr.split('.');
    if (parts.length === 3) {
        return new Date(parts[2], parts[1] - 1, parts[0]);
    } else {
        console.error('Date string is not in the expected format:', dateStr);
        return null;
    }
}

function toggleRandomBoolean(selector) {
    const state = Math.random() > 0.5 ? 'fa-toggle-on' : 'fa-toggle-off';
    $(selector).removeClass('fa-toggle-on fa-toggle-off').addClass(state);
}

function toggleBoolean(featureId) {
    $('#' + featureId).toggleClass('fa-toggle-on fa-toggle-off');
}

function getColorForCity(city) {
    let hash = 0;
    for (let i = 0; i < city.length; i++) {
        hash = city.charCodeAt(i) + ((hash << 5) - hash);
    }
    const color = (hash & 0x00FFFFFF).toString(16).toUpperCase();
    return "#" + "00000".substring(0, 6 - color.length) + color;
}

function determineRoomBracket(numberOfRooms) {
    if (numberOfRooms === 1) return '1 room';
    if (numberOfRooms === 2) return '2 rooms';
    if (numberOfRooms === 3) return '3 rooms';
    if (numberOfRooms === 4) return '4 rooms';
    if (numberOfRooms >= 5) return '5+ rooms';
    return 'Unknown';
}

function randomizeInputs() {
    const currentYear = new Date().getFullYear();

    const geographicSelect = document.getElementById('geographicSelect');
    const options = geographicSelect.querySelectorAll('option');
    const randomOptionIndex = Math.floor(Math.random() * (options.length - 1)) + 1;
    geographicSelect.value = options[randomOptionIndex].value;
    geographicSelect.dispatchEvent(new Event('change'));

    // Randomize land area between 20 and 200
    $('input[name="land_area"]').val(Math.floor(Math.random() * (200 - 20 + 1) + 20));

    // Randomize year of construction between some reasonable start year and the current year
    $('input[name="year_of_construction"]').val(Math.floor(Math.random() * (currentYear - 1950 + 1) + 1950));

    // Randomize number of rooms between 1 and 10
    $('input[name="rooms"]').val(Math.floor(Math.random() * (10 - 1 + 1) + 1));

    $('input[name="latitude"]').val(geographicSelect.getAttribute('data-latitude'));
    $('input[name="longitude"]').val(geographicSelect.getAttribute('data-longitude'));

    // Toggle binary features randomly
    toggleRandomBoolean('#liftToggle');
    toggleRandomBoolean('#parkingSpaceToggle');
    toggleRandomBoolean('#basementToggle');
    toggleRandomBoolean('#gazeboToggle');
    toggleRandomBoolean('#terraceToggle');
    toggleRandomBoolean('#poolToggle');
    toggleRandomBoolean('#airConditioningToggle');
    toggleRandomBoolean('#saunaToggle');
    toggleRandomBoolean('#balconyToggle');
    toggleRandomBoolean('#garageToggle');
    toggleRandomBoolean('#loggiaToggle');
    toggleRandomBoolean('#gardenToggle');
    toggleRandomBoolean('#fireplaceToggle');
    toggleRandomBoolean('#bathroomToggle');
    toggleRandomBoolean('#newBuildingToggle');
}

function unformatNumber(value) {
    value = value.replace(/\s*€\s*/g, '');
    value = value.replace(',', '.');
    value = value.replace(/\.\d{3}/g, match => match.replace('.', ''));
    return value;
}

function formatPrice(price) {
    const roundedPrice = price.toFixed(3);
    const parts = roundedPrice.split('.');
    const integerPart = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    const formattedPrice = `${integerPart},${parts[1]}€`;
    return formattedPrice;
}

function determineAgeBracket(age) {
    if (age <= 10) return '0-10 years';
    if (age <= 20) return '11-20 years';
    if (age <= 30) return '21-30 years';
    if (age <= 40) return '31-40 years';
    if (age <= 50) return '41-50 years';
    return 'Over 50 years';
}

function getColorForPrice(price) {
    return `rgba(255, ${255 - Math.min(price / 1000, 255)}, ${255 - Math.min(price / 1000, 255)}, 0.6)`;
}

function getRadiusForPrice(price) {
    return Math.max(5, Math.min(20, price / 100000));
}

function quartile(arr, q) {
    const sorted = arr.sort((a, b) => a - b);
    const pos = (sorted.length - 1) * q;
    const base = Math.floor(pos);
    const rest = pos - base;
    if (sorted[base + 1] !== undefined) {
        return sorted[base] + rest * (sorted[base + 1] - sorted[base]);
    } else {
        return sorted[base];
    }
}

/**
 * @param {ToastLevel} toastLevel
 * @param {string} title
 * @param {string} body
 */
function showToast(toastLevel, title, body) {
    var messageColored = `<i style="color: ${toastLevel}">${body}</i>`;
    var newToast = $('<div class="toast end-0 bottom-0 mx-3" style="width: 250px; margin-bottom: 10px;" role="alert" aria-live="assertive" aria-atomic="true">' +
        '<div class="toast-header">' +
        '<strong class="mr-auto">' + title + '</strong>' +
        '</div>' +
        '<div class="toast-body">' +
        messageColored +
        '</div>' +
        '</div>');

    $('.toast-container').prepend(newToast);
    let toast = new bootstrap.Toast(newToast[0]);
    toast.show();

    // Remove toast after it was displayed
    setTimeout(function () {
        newToast.remove();
    }, 7000);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.addEventListener('DOMContentLoaded', event => {
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
        });
    }

    $('[data-bs-toggle="tooltip"]').tooltip()

    const dropdownItems = document.querySelectorAll('.dropdown-item');
    const dropdown = document.getElementById('featureDropdown');
    var slider = document.getElementById('priceSlider');
    var minPriceInput = document.getElementById('minPrice');
    var maxPriceInput = document.getElementById('maxPrice');
    const selectedFeatures = [];
    dropdownItems.forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();
            const value = this.getAttribute('data-value');
            const index = selectedFeatures.indexOf(value);

            if (index > -1) {
                selectedFeatures.splice(index, 1);
                this.classList.remove('active');
            } else {
                selectedFeatures.push(value);
                this.classList.add('active');
            }

            dropdown.textContent = selectedFeatures.length > 0 ? `Selected: ${selectedFeatures.length}` : 'Select';
        });
    });

    var menu = document.querySelector('#featureDropdown + .dropdown-menu');
    if (menu) {
        menu.addEventListener('click', function (e) {
            e.stopPropagation();
        });
    }

    if (slider) {
        slider.noUiSlider.on('update', function (values, handle) {
            minPriceInput.value = formatNumber(values[0]);
            maxPriceInput.value = formatNumber(values[1]);
        });

        slider.noUiSlider.on('start', function (values, handle) {
            slider.querySelectorAll('.noUi-tooltip')[handle].style.display = 'block';
        });

        slider.noUiSlider.on('end', function () {
            slider.querySelectorAll('.noUi-tooltip').forEach(function (tooltip) {
                tooltip.style.display = 'none';
            });
        });
    }

    if (minPriceInput & maxPriceInput) {
        minPriceInput.addEventListener('change', function () {
            slider.noUiSlider.set([this.value, null]);
        });

        maxPriceInput.addEventListener('change', function () {
            slider.noUiSlider.set([null, this.value]);
        });

        [minPriceInput, maxPriceInput].forEach(input => {
            input.addEventListener('focus', function () {
                this.value = unformatNumber(this.value); // Remove formatting when focused
            });

            input.addEventListener('blur', function () {
                if (this.value.includes("€")) {
                    this.value = this.value;
                } else {
                    this.value = formatNumber(this.value);
                }
            });

            input.addEventListener('keypress', function (event) {
                if (event.key === 'Enter') {
                    event.preventDefault();
                    this.blur();
                }
            });
        });
    }
});

