from mtmenu.ui.popup import Popup
from mtmenu.settings import SCATTER_SIZE


class OrderMenu( Popup ):

    def __init__(self, **kwargs):
        kwargs.setdefault('title', 'Order by:')
        kwargs.setdefault('size', (210, 80))
        kwargs.setdefault('scale', 0.79)
        kwargs.setdefault('pos', (SCATTER_SIZE[0]-250, SCATTER_SIZE[1]-68))
        kwargs.setdefault('label_submit', 'Name')
        kwargs.setdefault('label_cancel', 'Runs')
        super(OrderMenu, self).__init__(**kwargs)

    
    def on_cancel(self):
        from mtmenu.ui import apps_grid
        apps_grid.reorder( order_by= 'runs' )
        
            
    def on_submit(self):
        from mtmenu.ui import apps_grid
        apps_grid.reorder( order_by= 'name' )
