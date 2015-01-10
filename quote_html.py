import sublime, sublime_plugin, re

class QuoteHtmlCommand(sublime_plugin.TextCommand):

	def run(self, edit, action='single'):
		view = self.view
		selection = view.sel()[0]

		if len(selection) > 0:
			regions = []
			for sel in view.sel():
				region = sublime.Region(
					view.line(min(sel.a, sel.b)).a,  # line start of first line
					view.line(max(sel.a, sel.b)).b   # line end of last line
				)
				code = view.substr(region)
				code = self.quote(code, action)
				view.replace(edit, region, code)

		else:
			region = sublime.Region(0, view.size())
			code = view.substr(region)
			code = self.quote(code, action)
			view.replace(edit, region, code)


	def quote(self, code, action):
		lines = code.split('\n')

		if action == 'double-ws':
			for i in range(len(lines)):
				lines[i] = re.sub(r'(?!\\)"', r'\\"', lines[i])
				lines[i] = re.sub(r'(\s*)(\S+(\s+\S+)*)\s*', r'"\1\2"', lines[i])

		elif action == 'double-wsn':
			for i in range(len(lines)):
				lines[i] = re.sub(r'(?!\\)"', r'\\"', lines[i])
				lines[i] = re.sub(r'(\s*)(\S+(\s+\S+)*)\s*', r'"\1\2\\n"', lines[i])
			lines[-1] = lines[len(lines) - 1][0:-3] + '"';

		elif action == 'double-wst':
			for i in range(len(lines)):
				lines[i] = re.sub(r'(?!\\)"', r'\\"', lines[i])
				lines[i] = re.sub(r'(\s*)(\S+(\s+\S+)*)\s*', r'_T("\1\2")', lines[i])

		elif action == 'double-wstn':
			for i in range(len(lines)):
				lines[i] = re.sub(r'(?!\\)"', r'\\"', lines[i])
				lines[i] = re.sub(r'(\s*)(\S+(\s+\S+)*)\s*', r'_T("\1\2\\n")', lines[i])
			lines[-1] = lines[len(lines) - 1][0:-4] + '")';

		elif action == 'double-wstrn':
			for i in range(len(lines)):
				lines[i] = re.sub(r'(?!\\)"', r'\\"', lines[i])
				lines[i] = re.sub(r'(\s*)(\S+(\s+\S+)*)\s*', r'_T("\1\2\\r\\n")', lines[i])
			lines[-1] = lines[len(lines) - 1][0:-6] + '")';

		code = '\n'.join(lines)

		return code