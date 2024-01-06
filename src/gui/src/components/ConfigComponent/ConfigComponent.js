import React from "react";
import Slider from '@mui/material/Slider';
import Avatar from '@mui/material/Avatar';
import MinervaIcon from '../../images/icon.jpeg';
import Stack from '@mui/material/Stack';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import WaveComponent from "./WaveComponent";
import Switch from '@mui/material/Switch';
import './Config.css';

const ConfigComponent = ({
    langVoices, voice, pitch, rate, volume, autoSpeak, isSpeaking,
    handleVoiceChange, handlePitchChange, handleRateChange, handleVolumeChange,
    handleAutoSpeakChange
}) => {
    return (
        <div className='Config'>
            <Stack direction="row" spacing={2}>
                <Avatar alt="Minerva" src={MinervaIcon} sx={{ width: 56, height: 56 }} />
                <h1>Minerva</h1>
            </Stack>
            <div>
                <label>
                    Voice:
                    <Select
                        labelId="select-voices"
                        id="select-voices-id"
                        value={voice ? voice.name : 'Select'}
                        onChange={handleVoiceChange}
                        label="Voices"
                        style={{width:'70%'}}
                    >
                        {langVoices.map((voice) => (
                        <MenuItem key={voice.name} value={voice.name}>
                            {voice.name}
                        </MenuItem>
                        ))}
                    </Select>
                </label>

                <br />

                <label>
                    Pitch:
                    <Slider
                        min={0.5}
                        max={2}
                        step={0.1}
                        value={pitch}
                        defaultValue={pitch}
                        onChange={handlePitchChange}
                    />
                </label>

                <br />

                <label>
                    Speed:
                    <Slider
                        min={0.5}
                        max={2}
                        step={0.1}
                        value={rate}
                        defaultValue={rate}
                        onChange={handleRateChange}
                    />
                </label>
                <br />
                <label>
                    Volume:
                    <Slider
                        min={0}
                        max={1}
                        step={0.1}
                        value={volume}
                        defaultValue={volume}
                        onChange={handleVolumeChange}
                    />
                </label>
                <br />
                <label>
                    Auto speak:
                    <Switch checked={autoSpeak} onChange={handleAutoSpeakChange}/>
                </label>
            </div>
            <WaveComponent isActive={isSpeaking}/>
        </div>
    );
}

export default ConfigComponent;