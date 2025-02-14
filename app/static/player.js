// Global variables for the player
let audio = new Audio();
let playlist = [];  // Array of track objects: { songId, songUrl, title, artist, album, coverImage }
let currentTrackIndex = 0;

// Helper function to format time in mm:ss
function formatTime(seconds) {
  if (isNaN(seconds)) return "0:00";
  let minutes = Math.floor(seconds / 60);
  let secs = Math.floor(seconds % 60);
  return minutes + ":" + (secs < 10 ? "0" + secs : secs);
}

// Save playlist and current index to localStorage
function savePlaylist() {
  localStorage.setItem("globalPlaylist", JSON.stringify(playlist));
  localStorage.setItem("currentTrackIndex", currentTrackIndex);
}

function updatePlayPauseButton() {
  const globalBtn = document.getElementById("playPauseBtn");
  const npBtn = document.getElementById("npPlayPauseBtn");
  if (globalBtn) globalBtn.textContent = audio.paused ? "⏯ Play" : "⏯ Pause";
  if (npBtn) npBtn.textContent = audio.paused ? "⏯ Play" : "⏯ Pause";
}

function updateCurrentSongInfo() {
  const infoDiv = document.getElementById("currentSongInfo");
  if (infoDiv && playlist[currentTrackIndex]) {
    infoDiv.textContent = "Playing: " + playlist[currentTrackIndex].title;
  }
}

function playSongAtIndex(index) {
  if (index < 0 || index >= playlist.length) {
    console.warn("Invalid track index:", index);
    return;
  }
  currentTrackIndex = index;
  let track = playlist[index];
  audio.src = track.songUrl;
  console.log("Playing track:", track);
  audio.load();
  audio.play().then(() => {
    console.log("Audio is playing:", audio.src);
  }).catch(error => {
    console.error("Audio playback error:", error);
  });
  updatePlayPauseButton();
  updateCurrentSongInfo();
  updateSongDetailsSidebar(track.title, track.artist, track.album, track.coverImage);
  savePlaylist();
}

function playSongDetailed(songId, songUrl, title, artist, album, coverImage) {
  console.log("playSongDetailed called with:", songId, songUrl, title, artist, album, coverImage);
  let track = { songId: songId, songUrl: songUrl, title: title, artist: artist, album: album, coverImage: coverImage };
  let index = playlist.findIndex(item => item.songUrl === songUrl);
  if (index === -1) {
    playlist.push(track);
    index = playlist.length - 1;
    console.log("Track added:", track);
  }
  playSongAtIndex(index);
  let detailsLink = document.getElementById("viewFullDetailsLink");
  if (detailsLink) {
    detailsLink.href = "/now_playing/" + songId;
    detailsLink.style.display = "inline-block";
  }
}

function playPause() {
  if (audio.paused) {
    audio.play().then(() => {
      console.log("Resumed playing.");
    }).catch(error => {
      console.error("Audio play error:", error);
    });
  } else {
    audio.pause();
    console.log("Audio paused.");
  }
  updatePlayPauseButton();
}

function nextTrack() {
  if (currentTrackIndex < playlist.length - 1) {
    playSongAtIndex(currentTrackIndex + 1);
  } else {
    console.log("No next track available.");
  }
}

function prevTrack() {
  if (currentTrackIndex > 0) {
    playSongAtIndex(currentTrackIndex - 1);
  } else {
    console.log("No previous track available.");
  }
}

// Update both the dashboard sidebar and Now Playing main details (if present)
function updateSongDetailsSidebar(title, artist, album, coverImage) {
  // Update dashboard sidebar if exists
  const titleElem = document.getElementById("songTitle");
  const artistElem = document.getElementById("songArtist");
  const albumElem = document.getElementById("songAlbum");
  const coverElem = document.getElementById("songCover");
  if (titleElem) titleElem.textContent = title;
  if (artistElem) artistElem.textContent = artist;
  if (albumElem) albumElem.textContent = "Album: " + album;
  if (coverElem) coverElem.src = coverImage;
  const sidebar = document.getElementById("songDetailsSidebar");
  if (sidebar) sidebar.style.display = "block";
  
  // Update Now Playing main details if present
  const npTitle = document.getElementById("npTitle");
  const npArtist = document.getElementById("npArtist");
  const npAlbum = document.getElementById("npAlbum");
  const npCover = document.getElementById("npCover");
  if (npTitle) npTitle.textContent = title;
  if (npArtist) npArtist.textContent = "Artist: " + artist;
  if (npAlbum) npAlbum.textContent = "Album: " + album;
  if (npCover) npCover.src = coverImage;
}

if (document.getElementById("progressBar")) {
  const progressBar = document.getElementById("progressBar");
  audio.addEventListener("timeupdate", function() {
    if (audio.duration) {
      let progress = (audio.currentTime / audio.duration) * 100;
      progressBar.value = progress;
      let currentTimeElem = document.getElementById("currentTime");
      let totalTimeElem = document.getElementById("totalTime");
      if (currentTimeElem) currentTimeElem.textContent = formatTime(audio.currentTime);
      if (totalTimeElem) totalTimeElem.textContent = formatTime(audio.duration);
    }
  });
  progressBar.addEventListener("input", function() {
    if (audio.duration) {
      let seekTime = (progressBar.value / 100) * audio.duration;
      audio.currentTime = seekTime;
    }
  });
}

// Helper function to format time as mm:ss
function formatTime(seconds) {
  if (isNaN(seconds)) return "0:00";
  let minutes = Math.floor(seconds / 60);
  let secs = Math.floor(seconds % 60);
  return minutes + ":" + (secs < 10 ? "0" + secs : secs);
}

document.addEventListener("DOMContentLoaded", function() {
  let storedPlaylist = localStorage.getItem("globalPlaylist");
  let storedIndex = localStorage.getItem("currentTrackIndex");
  if (storedPlaylist) {
    try {
      playlist = JSON.parse(storedPlaylist);
      currentTrackIndex = storedIndex ? parseInt(storedIndex) : 0;
      console.log("Loaded playlist:", playlist, currentTrackIndex);
    } catch (e) {
      console.error("Error loading playlist:", e);
      playlist = [];
      currentTrackIndex = 0;
    }
  }
  
  const prevBtn = document.getElementById("prevBtn");
  const playPauseBtn = document.getElementById("playPauseBtn");
  const nextBtn = document.getElementById("nextBtn");
  if (prevBtn) prevBtn.addEventListener("click", prevTrack);
  if (playPauseBtn) playPauseBtn.addEventListener("click", playPause);
  if (nextBtn) nextBtn.addEventListener("click", nextTrack);
  
  const npPrevBtn = document.getElementById("npPrevBtn");
  const npPlayPauseBtn = document.getElementById("npPlayPauseBtn");
  const npNextBtn = document.getElementById("npNextBtn");
  if (npPrevBtn) npPrevBtn.addEventListener("click", prevTrack);
  if (npPlayPauseBtn) npPlayPauseBtn.addEventListener("click", playPause);
  if (npNextBtn) npNextBtn.addEventListener("click", nextTrack);
});
