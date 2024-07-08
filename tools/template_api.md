
#### 接口信息
- **请求地址**: <span id="copy" style="cursor: pointer;">**`^请求地址^`**</span><span id="success" style="display: none; color:gray; margin-left:10px; ">复制成功&#x2705; </span> 
- **请求方式**: ^请求方式^
- **描述信息**: ^描述信息^
- **更新时间**: ^更新时间^

#### 请求参数
<!-- |名称|类型|必填|说明|
|-|-|:-:|-|-| -->
^请求参数^

#### 请求示例
^请求示例^

<script>
document.addEventListener('DOMContentLoaded', ()=> {
    var elementA = document.getElementById('copy');
    var elementB = document.getElementById('success');
    elementA.addEventListener('click', () => {
      var textToCopy = elementA.textContent || elementA.innerHTML;
      navigator.clipboard.writeText(textToCopy).then(()=> 
    {
       elementB.style.display = 'inline';
                 setTimeout(function() {
               elementB.style.display = 'none';
          }, 1000);
    }
  )
     });
});
</script>