import React, { useState } from 'react';
import axios from 'axios';
import { useSelector, useDispatch} from "react-redux";

const ScanAPI = "http://127.0.0.1:8000/scanners/api/scan_list/";


export default function ScanUpload() {

  const [image, setImage] = useState('');
  const [previewImage, setPreviewImage] = useState('');
  const [extractedText, setExtractedText] = useState('');

  // Redux Stuff
  const reduxState = useSelector((reduxState) => reduxState);


  const handleImageChange = (e) => {
    //setImage({image:URL.createObjectURL(e.target.files[0]),name: e.target.files[0].name});
    setImage(e.target.files[0]);
    setPreviewImage(URL.createObjectURL(e.target.files[0]))
  };

  const handleEditChange = (e) => {
    setExtractedText(e.target.value);
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(image);
    //console.log(this.state);
    let form_data = new FormData();
    form_data.append('image', image);
    form_data.append('property', reduxState.propertyList);
    form_data.append('user', 1);
    console.log(form_data);
    axios.post(ScanAPI, form_data, {
      headers: {
        'content-type': 'multipart/form-data'
      }
    })
        .then(res => {
          console.log(res.data);
          setExtractedText(res.data.raw_text);
        })
        .catch(err => console.log(err))
  };


  return (
    <div className="upload_wrapper">
      <form onSubmit={handleSubmit}>
        <p>
          <h4 className="debuggingText">Current property pk: {reduxState.propertyList}</h4>
        </p>
        <div>
          <img className="preview_image" src={previewImage} alt="preview image" />
        </div>
        <div>
          <textarea rows="6" wrap="soft" className="edit_box" value={extractedText} onChange={handleEditChange} />
        </div>
        <p>
          <input type="file"
                  id="image"
                  accept="image/png, image/jpeg"  onChange={handleImageChange} required/>
        </p>
        <input type="submit"/>
      </form>
    </div>
  );
  
}
