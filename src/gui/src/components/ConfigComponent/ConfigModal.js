import React from "react";
import Slider from '@mui/material/Slider';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import CloseIcon from '@mui/icons-material/Close';
import Switch from '@mui/material/Switch';
import Stack from '@mui/material/Stack';
import { IconButton } from "@mui/material";
import './Config.css';

const ConfigModal = ({
    langVoices, voice, pitch, rate, volume, autoSpeak, darkTheme,
    handleVoiceChange, handlePitchChange, handleRateChange, handleVolumeChange,
    handleAutoSpeakChange, handleClose, handleChangeDarkTheme
}) => {
    const theme = darkTheme ? "Dark Theme" : "Light Theme";

    return (
        <div className="ConfigModal">
            <Stack direction="row" spacing={30}>
                <h3>Configuration</h3>
                <IconButton onClick={handleClose}><CloseIcon color="primary"/></IconButton>
            </Stack>
            <hr/>
            <br/>
            <label>
                Voice:
                <Select
                    labelId="select-voices"
                    id="select-voices-id"
                    label="Voices"
                    value={voice ? voice.name : 'Select'}
                    onChange={handleVoiceChange}
                    color='primary'
                    style={{width:'70%', color: 'white'}}
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
            <label>
                {theme}:
                <Switch checked={darkTheme} onChange={handleChangeDarkTheme}/>
            </label>
        </div>
    )
}

export default ConfigModal;