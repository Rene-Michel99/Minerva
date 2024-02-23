import React, { useEffect, useState } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Toolbar from '@mui/material/Toolbar';
import Avatar from '@mui/material/Avatar';
import Stack from '@mui/material/Stack';
import MinervaIcon from './images/icon.jpeg';
import SidebarComponent from './components/SidebarComponent/SidebarComponent.js';
import ChatComponent from './components/ChatComponent/ChatComponent.js';
import './App.css';


function getDefaultVoice(voices) {
  const defaultVoice = voices.filter((voice) => {
    return voice.name.indexOf("Francisca") >= 0 ? voice : null;
  })[0];
  return defaultVoice !== undefined ? defaultVoice : voices[0];
}

function App(props) {
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const [isClosing, setIsClosing] = React.useState(false);
  const [langVoices, setLangVoices] = useState([]);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [voice, setVoice] = useState(null);
  const [pitch, setPitch] = useState(1);
  const [rate, setRate] = useState(1);
  const [volume, setVolume] = useState(1);
  const [autoSpeak, setAutoSpeak] = useState(true);
  const [darkTheme, setDarkTheme] = useState(false);
  const drawerWidth = 240;
  

  const handleVoiceChange = (event) => {
    setVoice(langVoices.find((v) => v.name === event.target.value));
  };

  const handlePitchChange = (event) => {
    setPitch(parseFloat(event.target.value));
  };

  const handleRateChange = (event) => {
    setRate(parseFloat(event.target.value));
  };

  const handleVolumeChange = (event) => {
    setVolume(parseFloat(event.target.value));
  };

  const handleAutoSpeakChange = () => {
    setAutoSpeak((previous) => !previous);
  }

  const handleSpeaking = (value) => {
    setIsSpeaking(value);
  }

  const handleDrawerClose = () => {
    setIsClosing(true);
    setMobileOpen(false);
  };

  const handleDrawerTransitionEnd = () => {
    setIsClosing(false);
  };

  const handleDrawerToggle = () => {
    if (!isClosing) {
      setMobileOpen(!mobileOpen);
    }
  };

  const handleChangeDarkTheme = () => {
    setDarkTheme((previous) => !previous);
    const currentTheme = document.querySelector("body").getAttribute("data-theme");
    if (currentTheme === null || currentTheme === "light") {
      document.querySelector("body").setAttribute("data-theme", "dark");
    } else {
      document.querySelector("body").setAttribute("data-theme", "light");
    }
  };

  useEffect(() => {
    const handleVoicesLoaded = () => {
      const avaiableVoices = window.speechSynthesis.getVoices().filter((v) => {
        return v ? v.lang === 'pt' || v.name.indexOf("Portuguese") >= 0 : null
      });
      setLangVoices(avaiableVoices);
      setVoice(getDefaultVoice(avaiableVoices));
    }
    window.speechSynthesis.addEventListener("voiceschanged", handleVoicesLoaded);

    handleVoicesLoaded();

    return () => {
      window.speechSynthesis.removeEventListener("voiceschanged", handleVoicesLoaded);
    }
  }, []);

  return (
    <Box className="App" >
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar className='AppBar'>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Stack direction="row" spacing={2}>
                <Avatar alt="Minerva" src={MinervaIcon} sx={{ width: 48, height: 48 }} />
                <h1>Minerva</h1>
            </Stack>
        </Toolbar>
      </AppBar>
      <SidebarComponent
        drawerWidth={drawerWidth}
        mobileOpen={mobileOpen}
        langVoices={langVoices}
        voice={voice}
        pitch={pitch}
        rate={rate}
        volume={volume}
        autoSpeak={autoSpeak}
        isSpeaking={isSpeaking}
        darkTheme={darkTheme}
        handleVoiceChange={handleVoiceChange}
        handlePitchChange={handlePitchChange}
        handleRateChange={handleRateChange}
        handleVolumeChange={handleVolumeChange}
        handleAutoSpeakChange={handleAutoSpeakChange}
        handleDrawerClose={handleDrawerClose}
        handleDrawerTransitionEnd={handleDrawerTransitionEnd}
        handleChangeDarkTheme={handleChangeDarkTheme}
      />
      <Box
        component="main"
        sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` } }}
      >
        <Toolbar />
        <ChatComponent
          voice={voice}
          pitch={pitch}
          rate={rate}
          volume={volume}
          isSpeaking={isSpeaking}
          autoSpeak={autoSpeak}
          handleSpeaking={handleSpeaking}
        />
      </Box>
    </Box>
  );
}

export default App;