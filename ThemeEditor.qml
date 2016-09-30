import QtQuick 2.1
import QtQuick.Layouts 1.3
import QtQuick.Window 2.1
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0
import org.kde.plasma.core 2.0 as PlasmaCore

Window {
	id: window
	width: 600
	height: 400
	x: (Screen.width - width) / 2
	y: (Screen.height - height) / 2
	visible: true

	property color themeAccentColor: "#000000"

	property bool loaded: false
	Component.onCompleted: loaded = true

	function toRGB(color) {
		return {
			'red': parseInt(color.toString().substr(1, 2), 16),
			'green': parseInt(color.toString().substr(3, 2), 16),
			'blue': parseInt(color.toString().substr(5, 2), 16),
		};
	}

	function toColorStr(color) {
		var rgb = toRGB(color);
		return rgb.red + ',' + rgb.green + ',' + rgb.blue
	}

	function setThemeColor(color) {
		themeAccentColor = color
		executable.exec('python3 ~/.local/share/plasma/desktoptheme/breeze-alphablack/setthemecolor.py ' + toColorStr(themeAccentColor))
	}



	PlasmaCore.DataSource {
		id: executable
		engine: "executable"
		connectedSources: []
		onNewData: disconnectSource(sourceName)

		function exec(cmd) {
			connectSource(cmd)
		}
	}

	ColumnLayout {
		anchors.fill: parent

		Text {
			text: "Choose a color"
			font.pixelSize: 24
		}

		RowLayout {
			Layout.fillWidth: true
			Layout.margins: 4

			Rectangle {
				height: 40
				width: 40
				color: window.themeAccentColor
			}

			TextField {
				id: colorField
				text: window.themeAccentColor
				onTextChanged: {
					if (!window.loaded) return;

					if (text.charAt(0) === '#' && text.length == 7) {
						window.setThemeColor(text)
					}
				}
			}
		}

		Text {
			text: "Choose the color that will accent your panel and window borders"
		}

		ScrollView {
			Layout.fillWidth: true
			Layout.fillHeight: true

			GridView {
				id: colorGrid
				anchors.horizontalCenter: parent.horizontalCenter
				clip: true
				Layout.fillWidth: true
				Layout.fillHeight: true
				cellWidth: 48
				cellHeight: 48
				property int cellPadding: 2

				model: [
'#000000',
'#1B1B1B',
'#555555',
'#696969',
'#A9A9A9',
'#A9A9A9',
'#848482',
'#3B3C36',
'#828E84',
'#534B4F',
'#555D50',
'#B2BEB5',
'#6E7F80',
'#F2F3F4',
'#4D5D53',
'#232B2B',
'#78866B',
'#BFAFB2',
'#98817B',
'#3B444B',
'#8F9779',
'#54626F',
'#98777B',
'#1F262A',
'#4F3A3C',
'#7E5E60',
'#1A2421',
'#536872',
'#91A3B0',
'#8C92AC',
'#856088',
'#483C32',
'#483C32',
'#253529',
'#536878',
'#A17A74',
'#A3C1AD',
'#4A646C',
'#36454F',
'#86608E',
'#996666',
'#9F8170',
'#669999',
'#666699',
'#614051',
'#543D37',
'#563C5C',
'#66424D',
'#915C83',
'#986960',
'#5D3954',
'#8FBC8F',
'#2F4F4F',
'#5F9EA0',
'#B48395',
'#87A96B',
'#704241',
'#A57164',
'#88654E',
'#856D4D',
'#A0785A',
'#918151',
'#355E3B',
'#AD6F69',
'#4F7942',
'#A67B5B',
'#A67B5B',
'#9B7653',
'#5D8AA8',
'#D1BEA8',
'#96C8A2',
'#58427C',
'#734F96',
'#B284BE',
'#A95C68',
'#E3DAC9',
'#F2F0E6',
'#3D2B1F',
'#333366',
'#A2A2D0',
'#79443B',
'#6F4E37',
'#40826D',
'#C4D8E2',
'#E5CCC9',
'#C2B280',
'#3B7A57',
'#5072A7',
'#301934',
'#843F5B',
'#A8516E',
'#703642',
'#81613C',
'#7BB661',
'#893F45',
'#BDB76B',
'#AF6E4D',
'#4B3621',
'#556B2F',
'#556B2F',
'#85BB65',
'#72A0C1',
'#92A1CF',
'#483D8B',
'#AB4B52',
'#BA8759',
'#C19A6B',
'#C19A6B',
'#C19A6B',
'#4E82B4',
'#965A3E',
'#6D9BC3',
'#9955BB',
'#664C28',
'#4B5320',
'#1E4D2B',
'#B94E48',
'#4A5D23',
'#779ECB',
'#F0EAD6',
'#BCD4E6',
'#6C3082',
'#702963',
'#873260',
'#592720',
'#CD9575',
'#B5A642',
'#ACE1AF',
'#2F847C',
'#8CBED6',
'#553592',
'#C154C1',
'#C154C1',
'#BF4F51',
'#954535',
'#C39953',
'#1B4D3E',
'#1B4D3E',
'#4682BF',
'#3C1414',
'#CC6666',
'#cc9966',
'#6699CC',
'#333399',
'#2E2D88',
'#9966CC',
'#6B4423',
'#6B4423',
'#654321',
'#EFDECD',
'#50C878',
'#CD607E',
'#DBE9F4',
'#2E5894',
'#D473D4',
'#D473D4',
'#C95A49',
'#CB6D51',
'#C74375',
'#F1DDCF',
'#665D1E',
'#A4C639',
'#CC4E5C',
'#F5F5DC',
'#966FD6',
'#B53389',
'#872657',
'#B87333',
'#DEB887',
'#6C541E',
'#9F2B68',
'#CB4154',
'#CC474B',
'#CD5B45',
'#BD33A4',
'#A52A2A',
'#A52A2A',
'#8A3324',
'#56A0D3',
'#4997D0',
'#28589C',
'#CC397B',
'#BF94E4',
'#C53151',
'#DA8A67',
'#CD7F32',
'#228B22',
'#9932CC',
'#D19FE8',
'#EFDFBB',
'#EFBBCC',
'#9C2542',
'#EDC9AF',
'#DE6FA1',
'#AB274F',
'#2A52BE',
'#E68FAC',
'#C72C48',
'#44D7A8',
'#177245',
'#ACE5EE',
'#ACE5EE',
'#DE5D83',
'#841B2D',
'#FEFEFA',
'#DDE26A',
'#801818',
'#B22222',
'#E1A95F',
'#DE5285',
'#A9203E',
'#E4717A',
'#F4C2C2',
'#E5AA70',
'#9FA91F',
'#2243B6',
'#DA3287',
'#7F1734',
'#C23B22',
'#AA381E',
'#7CB9E8',
'#AC1E44',
'#C32148',
'#E9967A',
'#F7E7CE',
'#21ABCD',
'#DE3163',
'#DE3163',
'#967117',
'#967117',
'#811453',
'#C41E3A',
'#D3212D',
'#CE2029',
'#B31B1B',
'#B31B1B',
'#E03C31',
'#E9D66B',
'#A1CAF1',
'#D2691E',
'#D2691E',
'#D2691E',
'#126180',
'#D891EF',
'#E0218A',
'#F19CBB',
'#E75480',
'#E34234',
'#E88E5A',
'#EEDC82',
'#B0BF1A',
'#1DACD6',
'#1DACD6',
'#8A2BE2',
'#E25822',
'#89CFF0',
'#E32636',
'#E97451',
'#FAEBD7',
'#188BC2',
'#E52B50',
'#4E1609',
'#F0DC82',
'#5DADEC',
'#1974D2',
'#318CE7',
'#6495ED',
'#0E7C61',
'#1560BD',
'#E936A7',
'#D71868',
'#EB4C42',
'#E9692C',
'#EA3C53',
'#1034A6',
'#EC3B83',
'#DC143C',
'#ED872D',
'#C46210',
'#ED9121',
'#FBCCE7',
'#480607',
'#FAF0BE',
'#9B870C',
'#F0E130',
'#EF3038',
'#F56FA1',
'#FAE7B5',
'#F7E98E',
'#0D98BA',
'#08457E',
'#1C1CF0',
'#B8860B',
'#CAE00D',
'#F88379',
'#F88379',
'#FBCEB1',
'#FAD6A5',
'#062A78',
'#056608',
'#4F86F7',
'#F64A8A',
'#D70A53',
'#F5C71A',
'#E4D00A',
'#08E8DE',
'#560319',
'#FA6E79',
'#3D0C02',
'#8806CE',
'#FDD5B1',
'#FBEC5D',
'#568203',
'#FF2052',
'#FC8EAC',
'#FB607F',
'#013220',
'#7C0A02',
'#FD7C6E',
'#03C03C',
'#014421',
'#FD6C9E',
'#84DE02',
'#9EFD38',
'#FD3F92',
'#850101',
'#FE6F5E',
'#77B5FE',
'#1F75FE',
'#0247FE',
'#820000',
'#8B0000',
'#990000',
'#A40000',
'#CC0000',
'#FF4040',
'#FF0800',
'#FF2800',
'#FF3800',
'#FF7F50',
'#FF9966',
'#CC5500',
'#FFCBA4',
'#964B00',
'#FF9933',
'#FF7E00',
'#7B3F00',
'#FFE4C4',
'#FF8C00',
'#E48400',
'#FFEBCD',
'#FFAA1D',
'#FFA812',
'#FFA700',
'#FFFAF0',
'#FFF8E7',
'#FFBF00',
'#FFBF00',
'#FFF8DC',
'#FFD300',
'#FFE135',
'#FDEE00',
'#FFEF00',
'#FFFDD0',
'#737000',
'#FFF600',
'#FFFF99',
'#FFFF33',
'#FFFF31',
'#DFFF00',
'#D0FF14',
'#CCFF00',
'#CCFF00',
'#8DB600',
'#BFFF00',
'#7FFF00',
'#66FF00',
'#4AFF00',
'#006400',
'#008000',
'#00FF00',
'#C9FFE5',
'#00703C',
'#004225',
'#006B3C',
'#7FFFD4',
'#00563F',
'#006A4E',
'#006A4E',
'#00CC99',
'#004B49',
'#008B8B',
'#F0FFFF',
'#F0FFFF',
'#B2FFFF',
'#00FFFF',
'#00FFFF',
'#00FFFF',
'#00CED1',
'#00147E',
'#E7FEFF',
'#7DF9FF',
'#0093AF',
'#0095B6',
'#B9F2FF',
'#00B7EB',
'#00BFFF',
'#00BFFF',
'#007AA5',
'#007BA7',
'#007BA7',
'#00B9FB',
'#A6E7FF',
'#0087BD',
'#00416A',
'#0072BB',
'#F0F8FF',
'#003366',
'#3399FF',
'#1E90FF',
'#007FFF',
'#002E63',
'#0070FF',
'#0047AB',
'#0048BA',
'#00308F',
'#003399',
'#0018A8',
'#00008B',
'#00009C',
'#0000FF',
'#3F00FF',
'#6F00FF',
'#330066',
'#8F00FF',
'#9400D3',
'#BF00FF',
'#F4BBFF',
'#F4BBFF',
'#8B008B',
'#CC00CC',
'#FF77FF',
'#FF00FF',
'#A2006D',
'#F400A1',
'#FF1493',
'#FF1493',
'#FF007F',
'#FF55A3',
'#FFBCD9',
'#FFA6C9',
'#FF004F',
'#D70040',
'#BE0032',
'#FF91AF',
'#800020',
'#FF003F',
'#AF002A',
'#FF033E',
'#FF0038',
'#FFB7C5',
'#FFC1CC',
'#960018',
'#FF5470',
'#E30022',
'#00C4B0',

				]

				delegate: MouseArea {
					width: colorGrid.cellWidth
					height: colorGrid.cellHeight
					hoverEnabled: true
					cursorShape: Qt.PointingHandCursor

					Rectangle {
						anchors.fill: parent
						color: modelData

						border.width: colorGrid.cellPadding
						border.color: parent.containsMouse ? "#000" : "transparent"
					}

					onClicked: {
						window.setThemeColor(modelData)
					}
				}
			}
		}
	}
}