import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
    Button, Grid, Typography, TextField, FormHelperText,
    FormControl, Radio, RadioGroup, FormControlLabel, Collapse, Alert
} from "@mui/material";
import { useSession } from "./SessionContext";

const defaultProps = {
    update: false,
    voteToSkip: 2,
    guestCanPause: true,
    roomCode: null,
    updateCallBack: () => { },
}

export default function CreateRoomPage(props) {
    props = {
        ...defaultProps,
        ...props
    }

    const [guestCanPause, setGuestCanPause] = useState(props.guestCanPause);
    const [voteToSkip, setVoteToSkip] = useState(props.voteToSkip);
    const [errMsg, setErrMsg] = useState("");
    const [successMsg, setSuccessMsg] = useState("");
    const navigate = useNavigate();
    const { session } = useSession()

    const handleVotesChange = (e) => {
        setVoteToSkip(e.target.value);
    }

    const handleGuestCanPauseChange = (e) => {
        setGuestCanPause(e.target.value === 'true');
    }

    const handleRoomButtonPressed = () => {
        const body = {
            guest_can_pause: guestCanPause,
            vote_to_skip: voteToSkip
        };
        session.post("api/create-room", body)
            .then(response => response.data)
            .then(data => navigate("/room/" + data.code))
    }

    const handleUpdateButtonPressed = () => {
        const body = {
            guest_can_pause: guestCanPause,
            vote_to_skip: voteToSkip,
            code: props.roomCode
        };
        session.patch("api/update-room", body)
            .then(response => {
                if (response.status === 200) {
                    setSuccessMsg("Room Updated successfully!")
                    props.updateCallBack()
                }
                else {
                    setErrMsg("Error Updating room...")
                }
            })
    }

    const title = props.update ? "Update Room" : "Create a Room";

    function renderUpdateButtons() {
        return (
            <Grid item xs={12} align="center">
                <Button
                    color="primary"
                    variant="contained"
                    onClick={handleUpdateButtonPressed}
                >
                    Update Room
                </Button>
            </Grid>
        )
    }
    function renderCreateButtons() {
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Button
                        color="primary"
                        variant="contained"
                        onClick={handleRoomButtonPressed}
                    >
                        Create A Room
                    </Button>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button color="secondary" variant="contained" to="/" component={Link}>
                        Back
                    </Button>
                </Grid>
            </Grid>
        )
    }
    return (
        <Grid container spacing={1}>
            <Grid item xs={12} align="center">
                <Collapse in={errMsg !== "" || successMsg !== ""}>
                    {successMsg !== "" ? (
                        <Alert severity="success" onClose={() => setSuccessMsg("")}>{successMsg}</Alert>
                    ) : (
                        <Alert severity="error" onClose={() => setErrMsg("")}>{errMsg}</Alert>
                    )}
                </Collapse>
            </Grid>

            <Grid item xs={12} align="center">
                <Typography component="h4" variant="h4">
                    {title}
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <FormControl component="fieldset">
                    <FormHelperText>
                        <span style={{ display: 'block', textAlign: 'center' }}>Guest control of playback state.</span>
                    </FormHelperText>
                    <RadioGroup
                        row
                        defaultValue="true"
                        value={guestCanPause.toString()}
                        onChange={handleGuestCanPauseChange}
                    >
                        <FormControlLabel
                            value="true"
                            control={<Radio color="primary" />}
                            label="play/pause"
                            labelPlacement="bottom"
                        />
                        <FormControlLabel
                            value="false"
                            control={<Radio color="secondary" />}
                            label="No Control"
                            labelPlacement="bottom"
                        />
                    </RadioGroup>
                </FormControl>
            </Grid>
            <Grid item xs={12} align="center">
                <FormControl>
                    <TextField
                        required={true}
                        type="number"
                        defaultValue={voteToSkip}
                        inputProps={{
                            min: 1,
                            style: { textAlign: "center" }
                        }}
                        onChange={handleVotesChange}
                    />
                    <FormHelperText>
                        <span style={{ display: 'block', textAlign: 'center' }}>
                            Votes required to skip.
                        </span>
                    </FormHelperText>
                </FormControl>
            </Grid>
            {props.update ? renderUpdateButtons() : renderCreateButtons()}
        </Grid>
    );
}
