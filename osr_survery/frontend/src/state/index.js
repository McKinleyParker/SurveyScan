import {combineReducers} from "redux";
import propertyListReducer from "./propertyReducer";



// combine all the reducers
const reducers = combineReducers({
    propertyList: propertyListReducer
})

export default reducers