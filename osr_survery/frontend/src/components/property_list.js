import React, {useState, useEffect} from "react";
import axios from "axios";
import { useSelector, useDispatch} from "react-redux";
import { bindActionCreators } from "redux";
import {actionCreators} from "../state/action_creators/index";



const PropertyApi = "http://127.0.0.1:8000/scanners/api/property_list/";

export default function PropertyList() {
    const [propertyList, setPropertyList] = useState([]);
    const [selected, setSelected] = useState("");
    const [lat, setLat] = useState("");
    const [lon, setLon] = useState("");
    const [options, setOptions] = useState("");

    //redux hook
    const reduxState = useSelector((reduxState) => reduxState);
    const dispatch = useDispatch();
    const {uploadPropertyList, addNewProperty, setProperty} = bindActionCreators(actionCreators, dispatch);

    console.log(uploadPropertyList);
    console.log(addNewProperty);

    console.log(reduxState)

    useEffect(() => {
        const fetchData = async () => {
            const response = await axios.get(PropertyApi);
            console.log(response);

            const propertyListObject = response.data;


            let optionItems = propertyListObject.map((property) =>
                <option key={property.pk} value={property.pk}>{property.property_name}</option>
            );

            setPropertyList(response.data);
            setOptions(optionItems);

        }
        
        fetchData().catch(console.error);
    },[]);   

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

    // 

    const handleChoice = (e) => {
        console.log("you have chosen...poorly");
    }

    const handleSelection = (e) => {
        const selectedProperty = e.target.value;
        setSelected(selectedProperty);
        setProperty(selectedProperty);
    }

    return propertyList.length ? (
        <div className="property_list_wrapper">
            <h1>Existing Properties</h1>
            <div>
                {propertyList.map((building) => {
                    return (
                        <div key={building.property_name}>ID {building.pk}: {building.property_name}</div>
                    );
                })}
            </div>
            <div>
                <button onClick={handleChoice}>Choose Me</button>
                <button onClick={handleLocate}>Locate Me</button>
                <p>{lat}  ---  {lon}</p>
            </div>
            <div>
                <button onClick={() => addNewProperty(1)}>Add One</button>
                <button onClick={() => uploadPropertyList(1)}>Subtract One</button>
                <h5>Total: {reduxState.propertyList}</h5>
            </div>
            <div>
                <h2>Dropdown Menu</h2>
                <select onChange={handleSelection}>{options}</select>
            </div>
           
            
        </div>
    ) : (
        <h1>Still Loading</h1>
    )
}