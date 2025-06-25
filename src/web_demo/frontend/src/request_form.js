import React from 'react';
import {
  Input,
  Form,
  FormText,
  Button,
  Dropdown, DropdownToggle, DropdownMenu, DropdownItem,
} from 'reactstrap';
import ReactBootstrapSlider from 'react-bootstrap-slider';


const dropdownData = [
  {
    id: "1adb3684e0d6113205e4e59a",
    text: "Ngày Lễ Độc thân 11/11/2017 , có tới 197 tấn kỷ tử được bán hết trong vỏn vẹn một giờ đồng hồ."
  },
  {
    id: "8c5893be42e46daa81a67ae9",
    text: "Tháng 2/2018 , Carol qua đời ở tuổi 58 do các vấn đề về phổi và tim."
  },
  {
    id: "781ea338754bb2d09c13adbb",
    text: "Malaysia là một quốc gia đa dạng sinh vật siêu cấp với một lượng lớn các loài và có mức độ loài đặc hữu cao."
  },
  {
    id: "42f29b78e2ba53ac125739f1",
    text: "Thằng này gãy cẳng tay, ca mổ thường thôi, không phải loại khẩn cấp.",
  },
  {
    id: "8021010d649486f2c5783845",
    text: "Thế là mày vừa làm quen được chúng nó, vừa biết bố cục cái cơ sở y tế. ",
  },
  {
    id: "b70b007d8ae712d30b08c35a",
    text: "Ổng bảo mấy chuyến bay vũ trụ với việc lập thuộc địa ngoài không gian quan trọng cho tương lai loài người lắm. ",
  },
  {
    id: "b63e1a7831b5fb86ff38e247",
    text: "Kẻ thừa hưởng di sản có quyền cự tuyệt, trừ phi dụng tâm từ chối để lẩn tránh nghĩa vụ tài sản với tha nhân.",
  },
  {
    id: "70a7ec42a34f207143e212ee",
    text: "Trump Hotels buộc phải đệ trình đơn phá sản tự nguyện để nhận gói cứu trợ, duy trì hoạt động kinh doanh.",
  },
  {
    id: "asda",
    text: "Hợp đồng hữu điều kiện, kỳ thực, thành bại tại sự kiện. Sự kiện khởi, hợp đồng sinh; sự kiện diệt, hợp đồng vong. Tuỳ duyên hóa cảnh, đạo lý tại thử.",
  },
]

function RequestForm(props) {
  // Build a default text object for the text area

  const [inputValue, setInputValue] = React.useState("");

  return (
    <Form>
      <div className="precomputed-div">
        Enter your text or&nbsp;&nbsp;

        <Dropdown isOpen={props.dropdownOpen} toggle={props.toggleExamplesDropDown}>
          <DropdownToggle color="info" caret>
            choose an example
          </DropdownToggle>
          <DropdownMenu>
            {
              dropdownData.map(item => <DropdownItem value={`/?id=${item.id}`} onClick={() => setInputValue(item.text)}>{item.text}</DropdownItem>)
            }
          </DropdownMenu>
        </Dropdown>
      </div>

      <br />
      <Input type="textarea" style={{ height: "100px" }} name="text" id="strapInputText" rows="2" value={inputValue} onChange={(value) => {
        setInputValue(value.currentTarget.value);
      }} />
      <FormText>Don't know what to type? Try the "use a random sentence" option or explore samples from our <a href="s3://hiep-delta-bk/chunks_out_c/"> dataset</a> on S3.</FormText>
      <hr />
      <div className="precomputed-div">
        Transfer sentences to the target style&nbsp;&nbsp;
        <Dropdown class="dropdown-style-menu" isOpen={props.styleDropDownOpen} toggle={props.toggleStyleDropDown}>
          <DropdownToggle color="info" caret>
            {props.targetStyle === null ? "choose a target style" : props.targetStyle}
          </DropdownToggle>
          <DropdownMenu>
            <DropdownItem onClick={() => props.toggleStyle("Casual")}>Casual</DropdownItem>
            <DropdownItem onClick={() => props.toggleStyle("Coarse")}>Coarse</DropdownItem>
            <DropdownItem onClick={() => props.toggleStyle("Formal")}>Formal</DropdownItem>
            <DropdownItem onClick={() => props.toggleStyle("Chinese")}>Chinese</DropdownItem>
          </DropdownMenu>
        </Dropdown>
      </div>
      {/* <hr />
      paraphraser top-p sampling value = {props.settings.top_p_paraphrase}
      <br />
      <ReactBootstrapSlider
        value={props.settings.top_p_paraphrase}
        change={props.changeSliderParaphrase}
        id="top-p-slider-paraphrase"
        step={0.01}
        max={1.0}
        min={0.0}
        orientation="horizontal" />

      <FormText>The style transfer models were trained with p = 0.0, but feel free to experiment with this slider if the paraphrases are too close to the input. Increasing the p value results in more diverse paraphrases at the expense of content preservation.
        Refer to <a href="https://arxiv.org/pdf/1904.09751.pdf">Holtzman et al. 2019</a> for more details.</FormText>
      <hr /> */}

      <br />
      <br />
      
      

      Style transfer top-p sampling value = {props.settings.top_p_style}
      <br />

      <ReactBootstrapSlider
        value={props.settings.top_p_style}
        change={props.changeSliderStyle}
        id="top-p-slider-style"
        step={0.01}
        max={1.0}
        min={0.0}
        orientation="horizontal" />

    
      <FormText>Increasing the p value results in more diverse stylistic properties, but at the expense of content preservation. Experiment with this slider to get the desired output, you will get different output samples on each run for larger p values. Some styles seem to benefit from higher p values like 0.6 and 0.9 .</FormText>
      <hr />

      <Button color="primary" onClick={props.transferSentence}><span>Transfer!</span></Button>
    </Form>
  );
}

export default RequestForm;
