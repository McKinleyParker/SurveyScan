

export const uploadPropertyList = (propertyList) => {
    return (dispatch) => {
        dispatch({
            type: "subtract", 
            payload: propertyList,
        })
    }
}

export const addNewProperty = (newProperty) => {
    return (dispatch) => {
        dispatch({
            type: "add", 
            payload: newProperty,
        })
    }
}
    
export const setProperty = (propertyChoice) => {
    return (dispatch) => {
        dispatch({
            type: "set", 
            payload: propertyChoice,
        })
    }
}
    