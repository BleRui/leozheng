<template>
    <div id="codeMirror">
        <codemirror style="height: auto;" v-model="codeData" :options="cmOptions"></codemirror>
    </div>
</template>

<script>
    import {codemirror} from 'vue-codemirror'

    // require styles
    import 'codemirror/lib/codemirror.css'

    // language js 支持语言
    import 'codemirror/mode/javascript/javascript.js'
    import 'codemirror/mode/python/python.js'
    // theme css 编辑器主题
    import 'codemirror/theme/base16-dark.css'
    import 'codemirror/theme/base16-light.css'
    import 'codemirror/theme/monokai.css'
    // closebrackets
    import 'codemirror/addon/edit/closebrackets.js'
    // keyMap
    import 'codemirror/mode/clike/clike.js'
    import 'codemirror/addon/edit/matchbrackets.js'
    import 'codemirror/addon/comment/comment.js'
    import 'codemirror/addon/dialog/dialog.js'
    import 'codemirror/addon/dialog/dialog.css'
    import 'codemirror/addon/search/searchcursor.js'
    import 'codemirror/addon/search/search.js'
    import 'codemirror/keymap/emacs.js'

    export default {
        /**
         * 参考: https://codemirror.net/
         * @param {string} code 展示代码
         * @param {string} mode 代码类型(js和python) 'text/javascript' 和 'text/x-python'
         * @param {string} theme 编码区风格 'base16-dark', 'base16-light', 'monokai'
         * 更多支持语言和风格请参考官方文档，引入即可
         * */
        name: 'CWCodeMirror',
        components: {
            codemirror
        },
        props: {
            code: {},
            mode: {
                default: 'text/javascript'
            },
            theme: {
                default: 'base16-dark'
            }
        },
        watch: {
            codeData() {
                this.$emit('changeData', this.codeData)
            }
        },
        data() {
            return {
                codeData: this.code,
                cmOptions: {
                    // codemirror options
                    tabSize: 4,
                    mode: this.mode,
                    theme: this.theme,
                    lineNumbers: true,
                    line: true,
                    foldgutter: true,
                    lineWrapping: true, //代码折叠
                    foldGutter: true,
                    matchBrackets: true, //括号匹配
                    autoCloseBrackets: true,
                    styleActiveLine: true,
                    keyMap: 'emacs'
                    // more codemirror options, 更多 codemirror 的高级配置...
                }
            }
        },
    }
</script>

<style>
    .CodeMirror {
        border: 1px solid #eee;
        height: auto;
        min-height: 100px;
    }

    .CodeMirror-scroll {
        height: auto;
        overflow-y: hidden;
        overflow-x: auto;
    }
</style>
