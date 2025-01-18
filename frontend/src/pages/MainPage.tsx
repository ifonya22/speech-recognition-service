import DragAndDropComponent from "../components/DragAndDropComponent";
import TextAreaComponent from "../components/TextAreaComponent";
import SelectComponent from "../components/SelectComponent";
import ButtonComponent from "../components/ButtonComponent";

const MainPage = () => {
    return (
        <div>
            <DragAndDropComponent/>
            <br />
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '20px' }}>
      <SelectComponent />
      <ButtonComponent />
    </div>
            
            
            
            <br />
            <TextAreaComponent/>
        </div>
    );
};

export default MainPage;