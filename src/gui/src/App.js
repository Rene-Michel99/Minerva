import React, { useEffect, useState } from 'react';
import './App.css';
import ConfigComponent from './components/ConfigComponent/ConfigComponent.js'
import ChatComponent from './components/ChatComponent/ChatComponent.js';


function getDefaultVoice(voices) {
  const defaultVoice = voices.filter((voice) => {
    return voice.name.indexOf("Francisca") >= 0 ? voice : null;
  })[0];
  return defaultVoice !== undefined ? defaultVoice : voices[0];
}

function App() {
  const [langVoices, setLangVoices] = useState([]);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [voice, setVoice] = useState(null);
  const [pitch, setPitch] = useState(1);
  const [rate, setRate] = useState(1);
  const [volume, setVolume] = useState(1);
  const [autoSpeak, setAutoSpeak] = useState(true);
  

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
    <div className='App'>
      <ConfigComponent
        langVoices={langVoices}
        voice={voice}
        pitch={pitch}
        rate={rate}
        volume={volume}
        autoSpeak={autoSpeak}
        isSpeaking={isSpeaking}
        handleVoiceChange={handleVoiceChange}
        handlePitchChange={handlePitchChange}
        handleRateChange={handleRateChange}
        handleVolumeChange={handleVolumeChange}
        handleAutoSpeakChange={handleAutoSpeakChange}
      />
      <ChatComponent
        voice={voice}
        pitch={pitch}
        rate={rate}
        volume={volume}
        isSpeaking={isSpeaking}
        autoSpeak={autoSpeak}
        handleSpeaking={handleSpeaking}
      />
    </div>
  );
}

export default App;
