import React, {useState} from "react";
import axios from "axios";
import { useSelector, useDispatch} from "react-redux";
import { bindActionCreators } from "redux";
import {actionCreators} from "../state/action_creators/index";


const noteAPI = "http://127.0.0.1:8000/scanners/api/note_list/";
/*
const fake_headers = {
    'Authorization': 'Bearer my-auth-token',
    'Custom-Header': 'xxxx-xxxx-xxxx-xxxx'
  };

  const headers = {
    'Access-Control-Allow-Origin': '*'
  }
*/


function PostTest() {
    // make a hook to capture API response
    const [note, setNote] = new useState("");

    // Redux Stuff
    const reduxState = useSelector((reduxState) => reduxState);

    const handleSubmit = () => {
        
        const data = {user: 1, 
                note_text: note};
        console.log("it is done");
        console.log(data)
        axios.post(noteAPI, data)
        .then(response => {
        console.log("Status: ", response.status);
        console.log("Data: ", response.data);
        console.log("well something is happening");
        }).catch(error => {
        console.error('Something went wrong!', error);
        });

    }





    
    const updateText = (e) => {
        setNote(e.target.value);
        console.log(note)
      };
    

    return (
        <div className='post_wrapper' >
            <h2>New Scan Upload</h2>
                <input type="text" onChange={updateText}/>
                <button type="submit" className="submit_btn" onClick={handleSubmit}>Submit</button>
            <h5>Grand Total: {reduxState.propertyList}</h5>
        </div>
    );

}

export default PostTest;