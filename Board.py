class Board:
    def __init__(self, canvas=None):
        self.wide = 355
        self.height = 710
        self.g = 9.809
        self.item = None
        self.canvas = canvas
        self.loss = 0.55

    def paint(self, root):
        if self.canvas is None:
            return

        board = self.canvas(root, bg='brown')
        board.place(x=85, y=85, width=384, height=742)

        self.item = self.canvas(root, bg='dark green')
        self.item.place(x=100, y=100, width=356, height=712)
        self.item.create_line(0, 565, 356, 565, fill='white')
        self.item.create_arc(
            120, 507, 236, 623,
            start=180, extent=180, style='arc', outline='white'
        )
        self.item.create_oval(
            176, 563, 180, 567, fill='white', outline='white')
        self.item.create_oval(176, 63, 180, 67, fill='white', outline='white')
        self.item.create_oval(
            176, 176, 180, 180, fill='white', outline='white')
        self.item.create_oval(
            176, 354, 180, 358, fill='white', outline='white')

    def paint_balls(self, balls):
        for ball in balls:
            ball.update_guess_coordinates()
            ball.paint(self.item)
