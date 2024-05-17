// Genres
document.getElementById('input-genres').addEventListener('input', function () {
  const input = this.value.trim().toLowerCase();
  const suggestions = document.getElementById('genre-suggestions');

  const validGenres = `Short Drama Comedy Cocumentary Adult Action Thriller Romance Animation Family Horror Crime Adventure Fantasy Sci_Fi Mystery Biography History Sport Musical War Western Film_noir`.split(' ');

  suggestions.innerHTML = '';

  const matchedGenres = validGenres.filter(genre => genre.toLowerCase().includes(input));

  matchedGenres.forEach(genre => {
    const suggestionItem = document.createElement('div');
    suggestionItem.textContent = genre;
    suggestionItem.classList.add('genre-suggestion');
    suggestionItem.addEventListener('click', function () {
      document.getElementById('input-genres').value = this.textContent;
      suggestions.innerHTML = '';
    });
    suggestions.appendChild(suggestionItem);
    suggestions.style.display = 'block';
  });
});

document.addEventListener('click', function (event) {
  const genresSuggestions = document.getElementById('genre-suggestions');
  const clickedElement = event.target;

  if (!genresSuggestions.contains(clickedElement)) {
    genresSuggestions.style.display = 'none';
  }
});

document.getElementById('add-genre-btn').addEventListener('click', function () {
  const genresInput = document.getElementById('input-genres');
  const genresList = document.getElementById('genres-list');
  const genreValue = genresInput.value.trim();

  const validGenres = `short drama comedy documentary adult action thriller romance animation family horror crime adventure fantasy sci_Fi mystery biography history sport musical war western film_noir`.split(' ');

  if (validGenres.includes(genreValue.toLowerCase())) {
    const genreItem = document.createElement('div');
    genreItem.classList.add('genre-item');
    genreItem.textContent = genreValue;

    const removeButton = document.createElement('button');
    removeButton.textContent = 'X';
    removeButton.classList.add('remove-btn');
    removeButton.addEventListener('click', function () {
      genresList.removeChild(genreItem);
    });

    genreItem.appendChild(removeButton);
    genresList.appendChild(genreItem);

    genresInput.value = '';
  } else {
    alert('Invalid genre!');
  }
});

const validCountry = [
  "Afghanistan",
  "Albania",
  "Algeria",
  "Andorra",
  "Angola",
  "Antigua and Barbuda",
  "Argentina",
  "Armenia",
  "Australia",
  "Austria",
  "Azerbaijan",
  "Bahamas",
  "Bahrain",
  "Bangladesh",
  "Barbados",
  "Belarus",
  "Belgium",
  "Belize",
  "Benin",
  "Bhutan",
  "Bolivia",
  "Bosnia and Herzegovina",
  "Botswana",
  "Brazil",
  "Brunei",
  "Bulgaria",
  "Burkina Faso",
  "Burundi",
  "Côte d'Ivoire",
  "Cabo Verde",
  "Cambodia",
  "Cameroon",
  "Canada",
  "Central African Republic",
  "Chad",
  "Chile",
  "China",
  "Colombia",
  "Comoros",
  "Congo (Congo-Brazzaville)",
  "Costa Rica",
  "Croatia",
  "Cuba",
  "Cyprus",
  "Czechia (Czech Republic)",
  "Democratic Republic of the Congo",
  "Denmark",
  "Djibouti",
  "Dominica",
  "Dominican Republic",
  "Ecuador",
  "Egypt",
  "El Salvador",
  "Equatorial Guinea",
  "Eritrea",
  "Estonia",
  "Eswatini",
  "Ethiopia",
  "Fiji",
  "Finland",
  "France",
  "Gabon",
  "Gambia",
  "Georgia",
  "Germany",
  "Ghana",
  "Greece",
  "Grenada",
  "Guatemala",
  "Guinea",
  "Guinea-Bissau",
  "Guyana",
  "Haiti",
  "Holy See",
  "Honduras",
  "Hungary",
  "Iceland",
  "India",
  "Indonesia",
  "Iran",
  "Iraq",
  "Ireland",
  "Israel",
  "Italy",
  "Jamaica",
  "Japan",
  "Jordan",
  "Kazakhstan",
  "Kenya",
  "Kiribati",
  "Kuwait",
  "Kyrgyzstan",
  "Laos",
  "Latvia",
  "Lebanon",
  "Lesotho",
  "Liberia",
  "Libya",
  "Liechtenstein",
  "Lithuania",
  "Luxembourg",
  "Madagascar",
  "Malawi",
  "Malaysia",
  "Maldives",
  "Mali",
  "Malta",
  "Marshall Islands",
  "Mauritania",
  "Mauritius",
  "Mexico",
  "Micronesia",
  "Moldova",
  "Monaco",
  "Mongolia",
  "Montenegro",
  "Morocco",
  "Mozambique",
  "Myanmar (formerly Burma)",
  "Namibia",
  "Nauru",
  "Nepal",
  "Netherlands",
  "New Zealand",
  "Nicaragua",
  "Niger",
  "Nigeria",
  "North Korea",
  "North Macedonia",
  "Norway",
  "Oman",
  "Pakistan",
  "Palau",
  "Palestine State",
  "Panama",
  "Papua New Guinea",
  "Paraguay",
  "Peru",
  "Philippines",
  "Poland",
  "Portugal",
  "Qatar",
  "Romania",
  "Russia",
  "Rwanda",
  "Saint Kitts and Nevis",
  "Saint Lucia",
  "Saint Vincent and the Grenadines",
  "Samoa",
  "San Marino",
  "Sao Tome and Principe",
  "Saudi Arabia",
  "Senegal",
  "Serbia",
  "Seychelles",
  "Sierra Leone",
  "Singapore",
  "Slovakia",
  "Slovenia",
  "Solomon Islands",
  "Somalia",
  "South Africa",
  "South Korea",
  "South Sudan",
  "Spain",
  "Sri Lanka",
  "Sudan",
  "Suriname",
  "Sweden",
  "Switzerland",
  "Syria",
  "Tajikistan",
  "Tanzania",
  "Thailand",
  "Timor-Leste",
  "Togo",
  "Tonga",
  "Trinidad and Tobago",
  "Tunisia",
  "Turkey",
  "Turkmenistan",
  "Tuvalu",
  "Uganda",
  "Ukraine",
  "United Arab Emirates",
  "United Kingdom",
  "United States",
  "Uruguay",
  "Uzbekistan",
  "Vanuatu",
  "Venezuela",
  "Vietnam",
  "Yemen",
  "Zambia",
  "Zimbabwe"
];

// Country
document.getElementById('input-country').addEventListener('input', function () {
  const input = this.value.trim().toLowerCase();
  const suggestions = document.getElementById('country-suggestions');

  suggestions.innerHTML = '';

  const matchedCountries = validCountry.filter(country => country.toLowerCase().includes(input));

  matchedCountries.forEach(country => {
    const suggestionItem = document.createElement('div');
    suggestionItem.textContent = country;
    suggestionItem.classList.add('country-suggestion');
    suggestionItem.addEventListener('click', function () {
      document.getElementById('input-country').value = this.textContent;
      suggestions.innerHTML = '';
    });
    suggestions.appendChild(suggestionItem);
    suggestions.style.display = 'block';
  });
});

document.addEventListener('click', function (event) {
  const genresSuggestions = document.getElementById('country-suggestions');
  const clickedElement = event.target;

  if (!genresSuggestions.contains(clickedElement)) {
    genresSuggestions.style.display = 'none';
  }
});

document.getElementById('add-country-btn').addEventListener('click', function () {
  const countryInput = document.getElementById('input-country');
  const countryList = document.getElementById('country-list');
  const countryValue = countryInput.value.trim();

  if (validCountry.includes(countryValue)) {
    const countryItem = document.createElement('div');
    countryItem.classList.add('country-item');
    countryItem.textContent = countryValue;

    const removeButton = document.createElement('button');
    removeButton.textContent = 'X';
    removeButton.classList.add('remove-btn');
    removeButton.addEventListener('click', function () {
      countryList.removeChild(countryItem);
    });

    countryItem.appendChild(removeButton);
    countryList.appendChild(countryItem);

    countryInput.value = '';
  } else {
    alert('Invalid country!');
  }
});

// Submit
function saveFormData() {
  // Lấy giá trị từ các trường input
  const movieName = document.getElementById('input-movie_name').value.trim();
  const month = document.getElementById('input-month').value;
  const year = document.getElementById('input-year').value;
  const mpaa = document.getElementById('input-mpaa').value;
  const runtime = document.getElementById('input-runtime').value.trim();
  const genresList = document.getElementById('genres-list');
  const countryList = document.getElementById('country-list');
  const genres = Array.from(genresList.children).map(genreItem => genreItem.textContent.trim().slice(0, -1)).join(', ');
  const country = Array.from(countryList.children).map(countryItem => countryItem.textContent.trim().slice(0, -1)).join(', ');
  const budget = document.getElementById('input-budget').value.trim();
  const screens = document.getElementById('input-screens').value.trim();
  const metaScore = document.getElementById('input-meta_score').value.trim();
  const ratings = document.getElementById('input-ratings').value.trim();
  const sequel = document.querySelector('input[name="input-sequel"]:checked').value;

  console.log("Movie Name:", movieName);
  console.log("Month:", month);
  console.log("Year:", year);
  console.log("MPAA:", mpaa);
  console.log("Runtime:", runtime);
  console.log("Genres:", genres);
  console.log("Country:", country);
  console.log("Budget:", budget);
  console.log("Screens:", screens);
  console.log("Meta Score:", metaScore);
  console.log("Ratings:", ratings);
  console.log("Sequel:", sequel);

  let data = {
    movieName: movieName,
    month: month,
    year: year,
    mpaa: mpaa,
    runtime: runtime,
    genres: genres,
    country: country,
    budget: budget,
    screens: screens,
    metaScore: metaScore,
    ratings: ratings,
    sequel: sequel
  };
  
  if (openingWeekDiv.style.display == "block") {
    const openingWeek = document.getElementById('input-opening_week').value.trim();
    console.log("Opening Week:", openingWeek);
    data.openingWeek = openingWeek;
  }
  
  fetch('/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
      // Xử lý kết quả từ Flask
      console.log(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  
}

document.addEventListener('DOMContentLoaded', function () {
  // Bắt sự kiện khi nhấn nút "Submit"
  document.querySelector('.submit-button').addEventListener('click', function (event) {
    // Ngăn chặn hành động mặc định của nút "Submit"
    event.preventDefault();

    // Gọi hàm để lấy giá trị từ form và lưu vào các biến
    saveFormData();
  });
});

const openingWeekRadioNo = document.getElementById('opening_week_0');
const openingWeekRadioYes = document.getElementById('opening_week_1');
const openingWeekDiv = document.getElementById('div-inp-opn-week');

openingWeekRadioNo.addEventListener('click', function () {
  openingWeekDiv.style.display = 'none';
});

openingWeekRadioYes.addEventListener('click', function () {
  openingWeekDiv.style.display = 'block';
});