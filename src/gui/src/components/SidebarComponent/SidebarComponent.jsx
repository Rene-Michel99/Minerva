import React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import ConfigComponent from '../ConfigComponent/ConfigComponent.js';


const SidebarComponent = ({
    drawerWidth, mobileOpen, langVoices, voice, pitch, rate, volume, autoSpeak,
    darkTheme, handleVoiceChange, handlePitchChange, handleRateChange, handleVolumeChange,
    handleAutoSpeakChange, handleDrawerClose, handleDrawerTransitionEnd, handleChangeDarkTheme
}) => {

    const drawer = (
        <ConfigComponent
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
            handleChangeDarkTheme={handleChangeDarkTheme}
        />
    );
    
    return (
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 }}}
        aria-label="mailbox folders"
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onTransitionEnd={handleDrawerTransitionEnd}
          onClose={handleDrawerClose}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
    );
}

export default SidebarComponent;