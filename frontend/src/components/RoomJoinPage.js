import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Grid, Typography, TextField, Button } from "@mui/material";
import { Link } from "react-router-dom";
import { useSession } from "./SessionContext";

export default function RoomJoinPage() {
    const [roomCode, setRoomCode] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();
    const { session } = useSession()

    function handleTextFieldChanges(e) {
        setRoomCode(e.target.value)
    }
    function roomButtonPressed(e) {
        // const requestOptions = {
        //     method: "POST",
        //     headers: { "Content-Type": "application/json" },
        //     body: JSON.stringify({
        //         code: roomCode
        //     })
        // };
        // fetch("http://localhost:8000/api/join-room", requestOptions)
        session.post("api/join-room", {code: roomCode})
            .then(response => {
                if (response.status===200) {
                    navigate(`/room/${roomCode}`)
                } else {
                    setError("Room Not Found.")
                }
            })
            .catch(err => {
                setError(err.response.data.error)

                console.log("Error:", err)
            })
    }

    return (
        <Grid container spacing={1}>
            <Grid item xs={12} align="center">
                <Typography variant="h4" component="h4">
                    Join a Room
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <TextField
                    error={!!error}
                    label="Code"
                    placeholder="Enter a room code"
                    value={roomCode}
                    helperText={error}
                    variant="outlined"
                    onChange={handleTextFieldChanges}
                />
            </Grid>
            <Grid item xs={12} align="center">
                <Button variant="contained" color="primary" onClick={roomButtonPressed}>
                    Enter Room
                </Button>
            </Grid>
            <Grid item xs={12} align="center">
                <Button variant="contained" color="secondary" to="/" component={Link}>
                    Back
                </Button>
            </Grid>
        </Grid>
    );
}
