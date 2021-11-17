

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
    
