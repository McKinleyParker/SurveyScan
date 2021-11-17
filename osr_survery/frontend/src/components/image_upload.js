import React from "react";
import { useForm } from "react-hook-form";
import axios from "axios";

const scan_upload_api = "http://127.0.0.1:8000/scanners/api/scan_list/"

const ScanUpload = () => {
  const { handleSubmit, register } = useForm({
    mode: "onBlur"
  });

  // const [imageFile, setImageFile] = useState(null);

  // const handleChange = e => {
  //   e.persist(); // per ParmentierChristophe react-hook-form/issues/274
  //   // console.log("e: ", e);
  //   setImageFile(e.target.files[0]); // oops. Nothing is there..
  //   console.log(imageFile);
  // };

  const fileInput = React.createRef();

  const onSubmitFn = data => {
    // event.preventDefault();  // I believe react-hook-form handles this
    console.log(
      "onSubmitFn:",
      data,
      "  imageFile: ",
      fileInput.current.files[0].name
    );
    const fd = new FormData();
    for (var key in data) {
      fd.append(key, data[key]); // formdata doesn't take objects
    }

    fd.append(
      "image",
      fileInput.current.files[0],
      fileInput.current.files[0].name
    );
    axios
      .post(scan_upload_api, fd, {
        onUploadProgress: ProgressEvent => {
          console.log(
            "Upload Progress: " +
              Math.round((ProgressEvent.loaded / ProgressEvent.total) * 100) +
              "%"
          );
        }
      })
      .then(res => {
        console.log("response from server: ", res);
      });
  };



  const testSubmit = data => {
    const form_data = new FormData();
    const url = "http://127.0.0.1:8000/scanners/api/scan_list/";

    form_data.append("property_name", "Always Water Ranch");
    form_data.append("address", "999 Desert Way");
    form_data.append("lat", 55);
    form_data.append("lon", 55);

    const config = {
      headers: {'content_type': 'multipart/form-data',
                'Access-Control_Allow-Origin': "*",}
    }

    axios.post(url, form_data, config)
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.log(error);
      });
  };

  return (
    <div className='upload_wrapper'>
      <h2>New Scan Upload</h2>
      <form onSubmit={handleSubmit(testSubmit)}>
        <div>
          <label htmlFor="avatar">Select a Photo</label>
          <input
            type="file"
            id="avatar"
            name="avatar"
            multiple
            ref={fileInput}
          />
        </div>


        <button type="submit" className="submit_btn">
          Submit
        </button>
      </form>
    </div>
  );
};

export default ScanUpload;
