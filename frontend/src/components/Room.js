import React, { useState, useEffect, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Button, Grid, Typography } from "@mui/material";
import CreateRoomPage from "./CreateRoomPage";
import { useSession } from "./SessionContext";
import MusicPlayer from "./MusicPlayer";

// const defaultSong = {
//     "title": "",
//     "artist": "",
//     "duration": 0,
//     "progress": 0,
//     "image_url": "",
//     "id": "",
//     "is_playing": false,
//     "votes": 0,
// }

export default function Room(props) {
    const [voteToSkip, setVoteToSkip] = useState(2);
    const [guestCanPause, setGuestCanPause] = useState(false);
    const [isHost, setIsHost] = useState(false);
    const [song, setSong] = useState({});
    const [spotifyAuthenticated, setSpotifyAuthenticated] = useState(false);
    const [showSettings, setShowSettings] = useState(false);
    const { roomCode } = useParams()
    const navigate = useNavigate()
    const {session} = useSession()

    function leaveButtonPressed() {
        session.post("api/leave-room")
            .then(_response => {
                navigate("/")
            })
    }
    
    const getRoomDetails = useCallback(() => {
        
        function authenticateSpotify() {
            session.get("spotify/is-authenticated")
                .then(response => response.data)
                .then(data => {
                    setSpotifyAuthenticated(data.status)
                    console.log("!data.status", !data.status)
                    if (!data.status) {
                        session.get("spotify/get-auth-url")
                            .then(response => response.data)
                            .then(data => {
                                window.location.replace(data.url);
                            })
                    }
                })
        }

        session.get(`api/get-room?code=${roomCode}`)
            .then(response => {
                if (response.status !== 200) {
                    props.leaveRoomCallBack();
                    navigate("/");
                }
                return response.data;
            })
            .then(data => {
                setVoteToSkip(data.vote_to_skip);
                setGuestCanPause(data.guest_can_pause);
                setIsHost(data.is_host);

                if (isHost) {
                    authenticateSpotify()
                }
            });
    }, [roomCode, props, navigate, session, setVoteToSkip, setGuestCanPause, setIsHost, isHost]);
    
    const getCurrentSong = useCallback(() => {
        session.get("spotify/get-current-song")
            .then(response => {
                if (response.status !== 200)
                    return {};
                return response.data;
            })
            .then(data => {
                console.log(data)
                setSong(data)
            })
    }, [session])

    useEffect(() => {
        getCurrentSong()
        
    }, [getCurrentSong])

    // const getCurrentSong = () => {
    //     try {
    //         session.get("spotify/get-current-song")
    //             .then(response => {
    //                 if (response.status !== 200)
    //                     return {};
    //                 return response.data;
    //             })
    //             .then(data => {
    //                 console.log(data)
    //                 setSong(data)
    //             })
    //     } catch (err) {
    //         console.log("Get Current Song:", err);
    //     }
    // }

    // const interval = setInterval(() => {
    //     getCurrentSong();
    // }, 1000);

    useEffect(() => {
        getRoomDetails()
        
        // return () => {
        //     clearInterval(interval);
        //     console.log("Cleared Interval");
        // }
    }, [getRoomDetails])

    // NOTE: Testing Behaviour
    useEffect(() => {
        const fetchData = () => {
            console.log("FETCHING DATA")
        }
        fetchData()
        return () => {
            console.log("RETURN FUNC")
        }
    }, [])
    

    function renderSettings(voteToSkip, guestCanPause, roomCode) {
        return <Grid container spacing={1}>
            <Grid item xs={12} align="center">
                <CreateRoomPage
                    update={true}
                    voteToSkip={voteToSkip}
                    guestCanPause={guestCanPause}
                    roomCode={roomCode}
                    updateCallBack={getRoomDetails}
                />
            </Grid>
            <Grid item xs={12} align="center">
                <Button
                    variant="contained"
                    color="secondary"
                    onClick={() => setShowSettings(false)}
                >
                    Close
                </Button>
            </Grid>
        </Grid>
    }

    function renderSettingsButton() {
        return (
            <Grid item xs={12} align="center">
                <Button
                    variant="contained"
                    color="primary"
                    onClick={() => setShowSettings(true)}
                >
                    Settings
                </Button>
            </Grid>
        )
    }

    if (showSettings) {
        return renderSettings(voteToSkip, guestCanPause, roomCode);
    }
    console.log("spotifyAuthenticated ::::::", spotifyAuthenticated);

    return (
        <Grid container spacing={1}>
            <Grid item xs={12} align="center">
                <Typography variant="h4" component="h4">
                    Code: {roomCode}
                </Typography>
            </Grid>
            {/* <Grid item xs={12} align="center">
                <Typography variant="h6" component="h6">
                    Votes: {voteToSkip}
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <Typography variant="h6" component="h6">
                    Guest can Pause: {guestCanPause.toString()}
                </Typography>
            </Grid> */}
            <Grid item xs={12} align="center">
                <Typography variant="h6" component="h6">
                    Host: {isHost.toString()}
                </Typography>
            </Grid>
            <MusicPlayer {...song}/>
            {isHost ? renderSettingsButton() : null}
            <Grid item xs={12} align="center">
                <Button variant="contained" color="secondary" onClick={leaveButtonPressed}>
                    Leave Room
                </Button>
            </Grid>
        </Grid>
    )
}

/* 
<div>
        <h3>{roomCode}</h3>
        <p>Votes: {voteToSkip}</p>
        <p>Guest can Pause: {guestCanPause.toString()}</p>
        <p>Host: {isHost.toString()}</p>
    </div>

*/