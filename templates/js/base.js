var $table = $('#fresh-table');

$(function () {
    $table.bootstrapTable({
        classes: 'table table-hover table-striped',
        toolbar: '.toolbar',
        striped: true,
        height: $(window).height(),
        columns: [
            {
					field: 'jianjie',
					title: '简介',
					align: 'left',
                    width: 100
             }, {
					field: 'dizhi',
					title: '地址',
					align: 'left',
                    width: 300,
					
					cellStyle:{
						css:{"word-wrap": "break-word"}
					}
             }, {
					field: 'caozuo',
					title: '操作',
					align: 'left',
					width: 50
             }
        ]
    })

    // 切换窗体时，防止错位
    $(window).resize(function () {
      $table.bootstrapTable('resetView', {
        height: $(window).height()
      })
    })
})