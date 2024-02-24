import React, { useState } from 'react';
import SettingsIcon from '@mui/icons-material/Settings';
import LiveHelpIcon from '@mui/icons-material/LiveHelp';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import Modal from "@mui/material/Modal";
import ConfigModal from "./ConfigModal";
import FAQModal from "./FAQModal";
import './Config.css';


const ConfigComponent = ({
    langVoices, voice, pitch, rate, volume, autoSpeak, isSpeaking,
    handleVoiceChange, handlePitchChange, handleRateChange, handleVolumeChange,
    handleAutoSpeakChange, handleChangeDarkTheme
}) => {

    const [modalConfigOpened, setModalConfigOpened] = useState(false);
    const [modalFAQOpened, setModalFAQOpened] = useState(false);

    const handleOpen = () => {
        setModalConfigOpened(true);
    }
    const handleClose = () => {
        setModalConfigOpened(false);
    }
    const handleFAQOpen = () => {
        setModalFAQOpened(true);
    }
    const handleFAQClose = () => {
        setModalFAQOpened(false);
    }

    return (
        <div className='Config'>
            <List >
                <ListItem disablePadding>
                    <ListItemButton onClick={handleOpen}>
                        <ListItemIcon><SettingsIcon color="primary"/></ListItemIcon>
                        <ListItemText primary={'Config'}/>
                    </ListItemButton>
                </ListItem>
                <Divider variant="fullWidth" component="li" sx={{ backgroundColor: 'gray' }} />
                <ListItem disablePadding>
                    <ListItemButton onClick={handleFAQOpen}>
                        <ListItemIcon><LiveHelpIcon color="primary"/></ListItemIcon>
                        <ListItemText primary={'Ajuda e FAQ'}/>
                    </ListItemButton>
                </ListItem>
            </List>
            <Modal
                open={modalConfigOpened}
                onClose={handleClose}
            >
                <ConfigModal
                    langVoices={langVoices}
                    voice={voice}
                    pitch={pitch}
                    rate={rate}
                    volume={volume}
                    autoSpeak={autoSpeak}
                    handleVoiceChange={handleVoiceChange}
                    handlePitchChange={handlePitchChange}
                    handleRateChange={handleRateChange}
                    handleVolumeChange={handleVolumeChange}
                    handleAutoSpeakChange={handleAutoSpeakChange}
                    handleClose={handleClose}
                    handleChangeDarkTheme={handleChangeDarkTheme}
                />
            </Modal>
            <Modal
                open={modalFAQOpened}
                onClose={handleFAQClose}
            >
                <FAQModal handleClose={handleFAQClose}/>
            </Modal>
        </div>
    );
}

export default ConfigComponent;