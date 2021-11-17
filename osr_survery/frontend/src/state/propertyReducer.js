const propertyListReducer = (state=100, action) => {
    switch (action.type) {
        case "add":
            return state + action.payload
        case "subtract":
            return state - action.payload;
        case "clear":
            return 0;
        default:
            return state;
    }
};

export default propertyListReducer