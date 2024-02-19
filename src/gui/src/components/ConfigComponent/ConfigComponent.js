import React, { useState } from 'react';
import SettingsIcon from '@mui/icons-material/Settings';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import Modal from "@mui/material/Modal";
import ConfigModal from "./ConfigModal";
import './Config.css';


const ConfigComponent = ({
    langVoices, voice, pitch, rate, volume, autoSpeak, isSpeaking, darkTheme,
    handleVoiceChange, handlePitchChange, handleRateChange, handleVolumeChange,
    handleAutoSpeakChange, handleChangeDarkTheme
}) => {

    const [modalOpened, setModalOpened] = useState(false);

    const handleOpen = () => {
        setModalOpened(true);
    }
    const handleClose = () => {
        setModalOpened(false);
    }

    return (
        <div className='Config'>
            <List>
                <ListItem disablePadding>
                    <ListItemButton onClick={handleOpen}>
                        <ListItemIcon><SettingsIcon color="primary"/></ListItemIcon>
                        <ListItemText primary={'Config'}/>
                    </ListItemButton>
                </ListItem>
                <Divider variant="fullWidth" component="li" sx={{ backgroundColor: 'gray' }} />
            </List>
            <Modal
                open={modalOpened}
                onClose={handleClose}
            >
                <ConfigModal
                    langVoices={langVoices}
                    voice={voice}
                    pitch={pitch}
                    rate={rate}
                    volume={volume}
                    autoSpeak={autoSpeak}
                    darkTheme={darkTheme}
                    handleVoiceChange={handleVoiceChange}
                    handlePitchChange={handlePitchChange}
                    handleRateChange={handleRateChange}
                    handleVolumeChange={handleVolumeChange}
                    handleAutoSpeakChange={handleAutoSpeakChange}
                    handleClose={handleClose}
                    handleChangeDarkTheme={handleChangeDarkTheme}
                />
            </Modal>
        </div>
    );
}

export default ConfigComponent;