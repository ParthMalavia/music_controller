import React from "react";
import { Grid, Typography, Card, IconButton, LinearProgress } from "@mui/material";
import { PlayArrow as PlayArrowButton, Pause as PauseButton, SkipNext as SkipNextButton } from "@mui/icons-material";
import { useSession } from "./SessionContext";

export default function MusicPlayer(props) {
    const songProgress = (props.progress / props.duration) * 100
    const { session } = useSession()

    function playSong() {
        session.put("spotify/play-song")
            .then(response => {
                if ("error" in response.data) {
                    alert(response.data.error.reason)
                }
            })
    }

    function pauseSong() {
        session.put("spotify/pause-song")
            .then(response => {
                if ("error" in response.data) {
                    alert(response.data.error.reason)
                }
            })
    }

    function skipSong() {
        session.post("spotify/skip-song")
            .then(response => {
                if ("error" in response.data) {
                    alert(response.data.error.reason)
                }
            })
    }

    return (
        <Card>
            <Grid container alignItems="center">
                <Grid item align="center" xs={4}>
                    <img src={props.image_url} alt="Loading ..." height="100%" width="100%" />
                </Grid>
                <Grid item align="center" xs={8}>
                    <Typography component="h5" variant="h5">
                        {props.title}
                    </Typography>
                    <Typography color="textSecondary" variant="subtitle1">
                        {props.artist}
                    </Typography>
                    <span>
                        <span>
                            <IconButton onClick={() => { props.is_playing ? pauseSong() : playSong() }}>
                                {props.is_playing ? <PlayArrowButton /> : <PauseButton />}
                            </IconButton>
                        </span>
                        <span>
                            <IconButton onClick={() => skipSong()}>
                                <SkipNextButton />
                            </IconButton>
                        </span>
                        <span>
                            <Typography color="textSecondary" variant="subtitle1">
                                {props.votes} / {props.votes_required}
                            </Typography>
                        </span>
                    </span>
                </Grid>
            </Grid>
            <LinearProgress variant="determinate" value={songProgress} />
        </Card>
    )
}
