import { Button, ButtonGroup, Grid, Typography } from "@mui/material";
import React, { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useSession } from './SessionContext'; // Import the useSession hook


export default function HomePage(props) {

    const {roomCode, setRoomCode} = props;
    const { session } = useSession();
    const navigate = useNavigate();

    async function callTest() {
        try {
            session.get('test')
            .then(response => console.log("RES", response))
        } catch (err) {
            console.log("callTest:", err);
        }
    }

    useEffect(() => {
        async function fetchRoomCode() {
            try {
                session.get("user-in-room")
                .then(response => setRoomCode(response.data.code))
            } catch (err) {
                console.log("User in room:", err);
            }
        }

        fetchRoomCode();
    }, [session, setRoomCode]);

    console.log("!!roomCode", !!roomCode)
    useEffect(() => {
        if (!!roomCode) {
            console.log("Before Redirect")
            navigate(`room/${roomCode}`);
            console.log("After Redirect")
        }
    }, [roomCode, navigate]);

    console.log("Func called")
    return (
        <Grid container spacing={3}>
            <Grid item xs={12} align="center">
                <Typography variant="h3" component="h3">House Party</Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <ButtonGroup disableElevation variant="contained" color="primary">
                    <Button color="primary" to="/join" component={Link}>
                        Join a Room
                    </Button>
                    <Button color="secondary" to="/create" component={Link}>
                        Create a Room
                    </Button>
                    {/* <Button color="primary" onClick={callTest} component={Link}>
                        Test
                    </Button> */}
                </ButtonGroup>
            </Grid>
        </Grid>
    )
}
