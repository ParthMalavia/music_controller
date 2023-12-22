import React, { useState } from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import CreateRoomPage from "./CreateRoomPage";
import HomePage from "./HomePage";
import Room from "./Room";
import RoomJoinPage from "./RoomJoinPage";


export default function RoutesPage() {
    const [roomCode, setRoomCode] = useState(null);

    function clearRoomCode() {
        setRoomCode(null);
    }

    return (
        <Router>
            <Routes>
                <Route path="/" Component={(props) => <HomePage {...props} roomCode={roomCode} setRoomCode={setRoomCode} clearRoomCode={clearRoomCode} />} />
                <Route path="create" Component={CreateRoomPage} />
                <Route path="room/:roomCode" Component={(props) => <Room {...props} leaveRoomCallBack={clearRoomCode} />} />
                <Route path="join" Component={RoomJoinPage} />
            </Routes>
        </Router>
    );
}
