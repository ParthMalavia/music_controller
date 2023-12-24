import React from "react";
import { Grid, Typography, Card, IconButton, LinearProgress } from "@mui/material";
import { PlayArrow as PlayArrowButton, Pause as PauseButton, SkipNext as SkipNextButton } from "@mui/icons-material";

export default function MusicPlayer(props) {
    console.log("MUSOC PLAYER PROPS ::", props)
    const songProgress = (props.progress / props.duration) * 100
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
                    <div>
                        <IconButton>
                            {props.is_playing ? <PlayArrowButton /> : <PauseButton />}
                        </IconButton>
                        <IconButton>
                            <SkipNextButton />
                        </IconButton>
                    </div>
                </Grid>
            </Grid>
            <LinearProgress variant="determinate" value={songProgress} />
        </Card>
    )
}
