<div>
<h4>The current state of Redux: {reduxState.propertyList[0].propertyName}</h4>
<button onClick={() => addNewProperty("grande hotel")}>Add another name</button>
<div>
    {reduxState.propertyList.map((building) => {
        return (
            <div key={building.propertyName}>Property Name: {building.propertyName}</div>
        );
    })}
</div>
</div>