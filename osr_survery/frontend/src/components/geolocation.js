import React, {useState, useEffect} from "react";
import axios from "axios";
import { useSelector, useDispatch} from "react-redux";
import { bindActionCreators } from "redux";
import {actionCreators} from "../state/action_creators/index";

// Choose location and select lat and lon
// user_lat_lon = {"lat":request.data["lat"], "lon":request.data["lon"]}


const NearbyPropertyApi = "http://127.0.0.1:8000/scanners/api/nearby_properties/";

export default function NearbyPropertyFinder() {
    const [propertyList, setPropertyList] = useState([]);
    // note to self: combine these into one hook
    const [lat, setLat] = useState("");  
    const [lon, setLon] = useState("");
    const [options, setOptions] = useState("");
    const [selected, setSelected] = useState("");

    //redux hook
    const reduxState = useSelector((reduxState) => reduxState);
    const dispatch = useDispatch();
    const {uploadPropertyList, addNewProperty, setProperty} = bindActionCreators(actionCreators, dispatch);

    const handleLocate = async () => {
        //navigator.geolocation.getCurrentPosition(function(position) {
        //console.log("Latitude is :", position.coords.latitude);
        //console.log("Longitude is :", position.coords.longitude);
        //});
        await navigator.geolocation.getCurrentPosition(position => {
            setLat(position.coords.latitude);
            setLon(position.coords.longitude);
            }); 
    }

    const nearbyRequestData = () => {
        const requestData = { params: 
                            {latitude: lat,
                            longitude: lon}
                            };
        return requestData;
    }
   

    const fetchData = async () => {
        const lat_lon = nearbyRequestData();
        console.log("Your request data looks like: ");
        console.log(lat_lon);
        const response = await axios.get(NearbyPropertyApi, lat_lon);
        console.log("Response: ");
        console.log(response);

        // same thing as the property listing module
        const propertyListObject = response.data;


        let optionItems = propertyListObject.map((property) =>
            <option key={property.pk} value={property.pk}>{property.property_name}</option>
        );

        setPropertyList(response.data);
        setOptions(optionItems);

    }
        
    const handleSelection = (e) => {
        console.log("this will update redux soon enough");
        const selectedProperty = e.target.value;
        setSelected(selectedProperty);
        setProperty(selectedProperty);
    }

    return  (
        <div className="property_list_wrapper">
            
            <div>
                <h1>Find Location</h1>
                <button onClick={handleLocate}>Locate Things</button>
                <b>Lat: {lat} ----- Lon: {lon}</b>
            </div>
            
            <div>
                <h1>Find Properties</h1>
                <button onClick={fetchData}>Fetch Things</button>
            </div>
            
            <div>
                <h1>Nearby Properties</h1>
                {propertyList.map((building) => {
                    return (
                        <div key={building.property_name}>ID {building.pk}: {building.property_name}</div>
                    );
                })}
                <select onChange={handleSelection}>{options}</select>
            </div>

        </div>
    ) 

}
