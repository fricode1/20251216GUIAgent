// 简化的 Markdown 解析器
// 这是一个轻量级的 Markdown 实现，支持常用的 Markdown 语法

function parseMarkdown(markdown) {
  let html = markdown;

  // 转义 HTML 特殊字符（除了我们生成的 HTML 标签）
  html = html.replace(/&/g, '&amp;');
  html = html.replace(/</g, '&lt;');
  html = html.replace(/>/g, '&gt;');

  // 代码块 (```code```)
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, function(match, lang, code) {
    return '<pre><code class="language-' + lang + '">' + code.trim() + '</code></pre>';
  });

  // 行内代码 (`code`)
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

  // 标题 (# ## ### #### ##### ######)
  html = html.replace(/^######\s+(.+)$/gm, '<h6>$1</h6>');
  html = html.replace(/^#####\s+(.+)$/gm, '<h5>$1</h5>');
  html = html.replace(/^####\s+(.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^###\s+(.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^##\s+(.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^#\s+(.+)$/gm, '<h1>$1</h1>');

  // 粗体和斜体
  html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
  html = html.replace(/___(.+?)___/g, '<strong><em>$1</em></strong>');
  html = html.replace(/__(.+?)__/g, '<strong>$1</strong>');
  html = html.replace(/_(.+?)_/g, '<em>$1</em>');

  // 链接 [text](url)
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');

  // 图片 ![alt](url)
  html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" />');

  // 无序列表
  html = html.replace(/^\* (.+)$/gm, '<li>$1</li>');
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');

  // 有序列表
  html = html.replace(/^\d+\. (.+)$/gm, '<oli>$1</oli>');
  html = html.replace(/(<oli>.*<\/oli>\n?)+/g, function(match) {
    return '<ol>' + match.replace(/<\/?oli>/g, '') + '</ol>';
  });

  // 引用块
  html = html.replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>');
  html = html.replace(/(<blockquote>.*<\/blockquote>\n?)+/g, function(match) {
    const content = match.replace(/<\/?blockquote>/g, '\n').trim();
    return '<blockquote>' + content.replace(/\n/g, '<br>') + '</blockquote>';
  });

  // 水平线
  html = html.replace(/^---$/gm, '<hr>');
  html = html.replace(/^\*\*\*$/gm, '<hr>');

  // 段落处理（不在标签内的文本行）
  const lines = html.split('\n');
  const result = [];
  let inList = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    // 跳过空行
    if (!line) {
      if (inList) {
        inList = false;
      }
      continue;
    }

    // 跳过已经是 HTML 标签的行
    if (line.match(/^<(h[1-6]|ul|ol|li|blockquote|pre|hr|div|p)/)) {
      result.push(line);
      continue;
    }

    // 普通文本行转换为段落
    if (!inList) {
      result.push('<p>' + line + '</p>');
    } else {
      result.push(line);
    }
  }

  html = result.join('\n');

  return html;
}

// 导出到全局
window.marked = {
  parse: parseMarkdown
};
