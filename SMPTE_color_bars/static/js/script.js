let currentFrequency = 0.00; // Set initial frequency to 0.00
const frequencyDisplay = document.getElementById('frequencyDisplay');
const channelDisplay = document.getElementById('channelDisplay'); // 채널 표시를 위한 요소
const frequencyDial = document.getElementById('frequencyDial');
const dialLever = document.getElementById('dialLever'); // 레버 추가
let rotation = 0; // 현재 레버 회전 각도
let currentChannel = 2; // Set initial channel to 2

// Display initial frequency and channel
frequencyDisplay.innerText = `Frequency: ${currentFrequency.toFixed(2)}`; // Frequency만 표시
channelDisplay.innerText = `Channel: ${currentChannel}`; // Channel은 따로 표시

const updateFrequency = () => {
  currentFrequency += 10.25; // Increase frequency by 10.25
  if (currentFrequency > 250) {
    currentFrequency = 0.00; // Reset to initial frequency if it exceeds 250
  }

  // Update display
  frequencyDisplay.innerText = `Frequency: ${currentFrequency.toFixed(2)}`; // Frequency만 표시
};

// Handle clicks on the dial and lever
const handleClick = () => {
  updateFrequency(); // Update frequency and display
  rotation += 30; // Click rotates lever by 30 degrees
  dialLever.style.transform = `translateX(-50%) rotate(${rotation}deg)`; // Rotate lever
};

// Start frequency increase on mouse down
const handleMouseDown = () => {
  updateFrequency(); // Initial frequency update
};

// Stop frequency increase on mouse up
const handleMouseUp = () => {
  clearInterval(interval); // Stop interval
};

frequencyDial.addEventListener('click', handleClick);
dialLever.addEventListener('click', handleClick);
dialLever.addEventListener('mousedown', handleMouseDown);
dialLever.addEventListener('mouseup', handleMouseUp);

// Selecting the power and antenna buttons
const powerButton = document.querySelector('.power-button');
const antennaButton = document.querySelector('.antenna-button');

// State variables for power and antenna
let isPowerOn = false; // Initially off
let isAntennaOn = false; // Initially off

// Function to toggle power on/off
const togglePower = () => {
  isPowerOn = !isPowerOn; // Toggle the state
  if (isPowerOn) {
    console.log('Power On'); // Log or update any visual cue
    powerButton.style.backgroundColor = '#0f0'; // Change button color to green when on
    // Add any other actions like turning on the TV screen here
  } else {
    console.log('Power Off'); // Log or update any visual cue
    powerButton.style.backgroundColor = '#555'; // Revert button color to original when off
    // Add any other actions like turning off the TV screen here
  }
};

// Function to toggle antenna on/off
const toggleAntenna = () => {
  isAntennaOn = !isAntennaOn; // Toggle the state
  if (isAntennaOn) {
    console.log('Antenna On'); // Log or update any visual cue
    antennaButton.style.backgroundColor = '#0f0'; // Change button color to green when on
    // Add any antenna-related functionality here
  } else {
    console.log('Antenna Off'); // Log or update any visual cue
    antennaButton.style.backgroundColor = '#555'; // Revert button color to original when off
    // Add any antenna-related functionality here
  }
};

// Event listeners for the buttons
powerButton.addEventListener('click', togglePower);
antennaButton.addEventListener('click', toggleAntenna);

// Handle Channel Up and Down buttons
const channelUpButton = document.querySelector('.channel-up-button');
const channelDownButton = document.querySelector('.channel-down-button');

// Update channel number display function
const updateChannel = () => {
  channelDisplay.innerText = `Channel: ${currentChannel}`; // Channel만 표시
};

// Handle Channel Up
const handleChannelUp = () => {
  currentChannel += 1; // Increment the channel
  if (currentChannel > 13) {
    currentChannel = 2; // Reset to channel 2 after exceeding 57
  }
  updateChannel(); // Update channel and frequency display
};

// Handle Channel Down
const handleChannelDown = () => {
  currentChannel -= 1; // Decrement the channel
  if (currentChannel < 2) {
    currentChannel = 13; // Wrap around to 57 if below 2
  }
  updateChannel(); // Update channel and frequency display
};

// Event listeners for Channel Up and Down buttons
channelUpButton.addEventListener('click', handleChannelUp);
channelDownButton.addEventListener('click', handleChannelDown);
