
from ..packages import *
from ..core import ANVIL, Exporter, NAMESPACE, PASCAL_PROJECT_NAME

__all__ = [ 'UIBindingType', 'UIElementType', 'UIAnchor', 'UIAnimType', 'UIEasing', 'UI']


class UIBindingType():
    View = 'view'
    Global = 'global'
class UIElementType():
    Image = 'image'
    Panel = 'panel'
    Label = 'label'
class UIAnchor():
    Center = 'center'
    TopLeft = 'top_left'
    TopMiddle = 'top_middle'
    TopRight = 'top_right'
    LeftMiddle = 'left_middle'
    RightMiddle = 'right_middle'
    BottomLeft = 'bottom_left'
    BottomMiddle = 'bottom_middle'
    BottomRight = 'bottom_right'
class UIAnimType():
    Alpha = 'alpha'
    Clip = 'clip'
    Color = 'color'
    Flip_book = 'flip_book'
    Offset = 'offset'
    Size = 'size'
    UV = 'uv'
    Wait = 'wait'
    Aseprite_flip_book = 'aseprite_flip_book'
class UIEasing():
    Linear = 'linear'
    Spring = 'spring'
    InQuad = 'in_quad'
    OutQuad = 'out_quad'
    InOutQuad = 'in_out_quad'
    InCubic = 'in_cubic'
    OutCubic = 'out_cubic'
    InOutCubic = 'in_out_cubic'
    InQuart = 'in_quart'
    OutQuart = 'out_quart'
    InOutQuart = 'in_out_quart'
    InQuint = 'in_quint'
    OutQuint = 'out_quint'
    InOutQuint = 'in_out_quint'
    InSine = 'in_sine'
    OutSine = 'out_sine'
    InOutSine = 'in_out_sine'
    InExpo = 'in_expo'
    OutExpo = 'out_expo'
    InOutExpo = 'in_out_expo'
    InCirc = 'in_circ'
    OutCirc = 'out_circ'
    InOutCirc = 'in_out_circ'
    InBounce = 'in_bounce'
    OutBounce = 'out_bounce'
    InOutBounce = 'in_out_bounce'
    InBack = 'in_back'
    OutBack = 'out_back'
    InOutBack = 'in_out_back'
    InElastic = 'in_elastic'
    OutElastic = 'out_elastic'
    InOutElastic = 'in_out_elastic'
class UIElementTrigger():
    Title = 'title'
    Actionbar = 'actionbar'
    NONE = None
class UIFontSize():
    Normal = 'normal'
    Small = 'small'
    Large = 'large'
    ExtraLarge = 'extra_large'

class _UIVariables(Exporter):
    def __init__(self) -> None:
        super().__init__('_global_variables', 'uivars')
        

    def add_variable(self, variable, value):
        self._content.update({
            variable : value
        })


class _UIBinding():
    def __init__(self) -> None:
        self._content = {}
    def binding_name(self, binding_name: str):
        self._content['binding_name'] = binding_name
        return self
    def binding_name_override(self, binding_name_override: str):
        self._content['binding_name_override'] = binding_name_override
        return self
    def binding_type(self, binding_type: UIBindingType =  UIBindingType.View):
        self._content['binding_type'] = binding_type
        return self
    def source_control_name(self, source_control_name: str):
        self._content['source_control_name'] = source_control_name
        return self
    def source_property_name(self, source_property_name: str):
        self._content['source_property_name'] = source_property_name
        return self
    def target_property_name(self, target_property_name: str):
        self._content['target_property_name'] = target_property_name
        return self


class _UIElement():
    def __init__(self, element_name: str) -> None:
        self._element_name = element_name
        self.element =  {
            'bindings' : [],
            'controls' : [],
            'variables': []
        }
        self._bindings : list[_UIBinding] = []
        self._controls : list[_UIElement] = []
    
    @property
    def should_steal_mouse(self):
        self.element['should_steal_mouse'] = True
        return self
        
    @property
    def absorbs_input(self):
        self.element['absorbs_input'] = True
        return self
    
    def visible(self, visible: bool | str):
        self.element['visible'] = visible
        return self
    
    def text(self, text: str):
        self.element['text'] = text
        return self
    
    def type(self, type: UIElementType):
        self.element['type'] = type
        return self

    def anchor(self, anchor_from: UIAnchor, anchor_to: UIAnchor):
        self.element['anchor_from'] = anchor_from
        self.element['anchor_to'] = anchor_to
        return self

    def text_alignment(self, text_alignment: UIAnchor):
        self.element['text_alignment'] = text_alignment
        return self

    def font_size(self, font_size: UIFontSize):
        self.element['font_size'] = font_size
        return self

    def layer(self, layer: int):
        self.element['layer'] = layer
        return self
    
    def texture(self, texture: str):
        CheckAvailability(f'{texture}.png', 'sprite', MakePath('assets', 'textures', 'ui'))
        self.element['texture'] = MakePath('textures', 'ui', texture)

        return self
    
    def keys(self, key, value):
        self.element[f'${key}'] = value
        return self
    
    @property
    def binding(self):
        bind = _UIBinding()
        self._bindings.append(bind)
        return bind
    
    def controls(self, element_name: str):
        ctrl = _UIElement(element_name)
        self._controls.append(ctrl)
        return ctrl

    def factory(self, name, id, element):
        self.element['factory'] = {
            "name": name,
            "control_ids": {
                id: element
            }
        }
        return self

    def size(self, size: str | tuple):
        self.element['size'] = size
        return self
    
    def uv(self, uv: tuple):
        self.element['uv'] = uv
        return self

    def uv_size(self, uv_size: tuple):
        self.element['uv_size'] = uv_size
        return self
    
    def alpha(self, alpha: str | tuple):
        self.element['alpha'] = alpha
        return self
    
    def offset(self, offset: str | tuple):
        self.element['offset'] = offset
        return self
    
    def clip_offset(self, clip_offset: tuple):
        self.element['clip_offset'] = clip_offset
        return self

    def keep_ratio(self, visible: bool):
        self.element['keep_ratio'] = visible
        return self
    
    def allow_clipping(self, allow_clipping: bool):
        self.element['allow_clipping'] = allow_clipping
        return self
    
    @property
    def shadow(self):
        self.element['shadow'] = True
        return self 
    
    @property
    def propagate_alpha(self):
        self.element['propagate_alpha'] = True
        return self

    def variables(self, requires: str, key, value):
        self.element['variables'].append({
            "requires": requires,
            f'${key}': value
        })
        return self
    
    @property
    def queue(self):
        for bind in self._bindings:
            self.element['bindings'].append(bind._content)
        for ctrl in self._controls:
            self.element['controls'].append(ctrl.queue)
        return { self._element_name: self.element }


class _UIAnimationElement():
    def __init__(self, animation_name: str) -> None:
        self._animation_name = animation_name
        self.animation =  {}
    
    def anim_type(self, anim_type: UIAnimType):
        self.animation['anim_type'] = anim_type
        return self

    def duration(self, duration: int | str):
        self.animation['duration'] = duration
        return self

    def next(self, next: str):
        self.animation['next'] = next
        return self

    def destroy_at_end(self, destroy_at_end: str):
        self.animation['destroy_at_end'] = destroy_at_end
        return self

    def play_event(self, play_event: str):
        self.animation['play_event'] = play_event
        return self
        
    def end_event(self, end_event: str):
        self.animation['end_event'] = end_event
        return self

    def start_event(self, start_event: str):
        self.animation['start_event'] = start_event
        return self

    def reset_event(self, reset_event: str):
        self.animation['reset_event'] = reset_event
        return self

    def easing(self, easing: UIEasing):
        self.animation['easing'] = easing
        return self
    
    def from_(self, from_: str | tuple):
        self.animation['from'] = from_
        return self
        
    def to(self, to: str | tuple):
        self.animation['to'] = to
        return self

    def initial_uv(self, initial_uv: tuple = (0, 0)):
        self.animation['initial_uv'] = initial_uv
        return self

    def fps(self, fps: int):
        self.animation['fps'] = fps
        return self

    def frame_count(self, frame_count: int):
        self.animation['frame_count'] = frame_count
        return self

    def frame_step(self, frame_step: int):
        self.animation['frame_step'] = frame_step
        return self

    @property
    def reversible(self):
        self.animation['reversible'] = True
        return self

    @property
    def resettable(self):
        self.animation['resettable'] = True
        return self

    @property
    def scale_from_starting_alpha(self):
        self.animation['scale_from_starting_alpha'] = True
        return self

    @property
    def activated(self):
        self.animation['activated'] = True
        return self

    @property
    def queue(self):
        return { self._animation_name: self.animation }

    def __str__(self) -> str:
        return self._animation_name


class _UIAnimation(Exporter):
    def __init__(self, name: str, namespace: str) -> None:
        super().__init__(name, 'uivars')
        self.namespace = namespace
        self._animations : list[_UIAnimationElement] = []
        self._content = {
            "namespace": namespace,
        }
        

    def add_animation(self, animation_name: str):
        self._animations.append(_UIAnimationElement(animation_name))
        return self._animations[-1]
    
    def queue(self, directory: str = ''):
        for anim in self._animations:
            self._content.update(anim.queue)
        return super().queue(directory)


class _UIScreen(Exporter):
    def __init__(self, name: str, namespace: str, anvil_animation : _UIAnimation, variables: _UIVariables) -> None:
        super().__init__(name, 'ui')
        self._content = {
            "namespace": namespace,
        }
        self.namespace = namespace
        self._elements : list[_UIElement] = []
        self._anvil_animation = anvil_animation
        self._variables = variables
        self._ignored_title_texts = []
        self._ignored_actionbar_texts = []
              
    def add_element(self, element_name: str, trigger: UIElementTrigger = UIElementTrigger.NONE, keyword: str = None):
        match trigger:
            case 'title':
                if not keyword is None:
                    self._variables.add_variable(f'$anvil.{element_name}.text', f'{NAMESPACE}:{keyword}')
                    self._variables.add_variable(f'$anvil.{element_name}.bool', f'(#text = $anvil.{element_name}.text)')
                    self._ignored_title_texts.append(f'(#text = $anvil.{element_name}.text)')

                factory = self.add_element(f'{element_name}_factory')
                factory.type(UIElementType.Panel)
                factory.factory('hud_title_text_factory', 'hud_title_text', f'{element_name}@anvil_hud.{element_name}')
            case 'actionbar':
                if not keyword is None:
                    self._variables.add_variable(f'$anvil.{element_name}.text', f'{NAMESPACE}:{keyword}')
                    self._variables.add_variable(f'$anvil.{element_name}.bool', f'($text = $anvil.{element_name}.text)')
                    self._ignored_title_texts.append(f'($text = $anvil.{element_name}.text)')
                factory = self.add_element(f'{element_name}_factory')
                factory.type(UIElementType.Panel)
                factory.factory('hud_actionbar_text_factory', 'hud_actionbar_text', f'{element_name}@anvil_hud.{element_name}')

        self._elements.append(_UIElement(element_name))
        return self._elements[-1]
    
    def queue(self, directory: str = ''):
        def copy_textures(element: _UIElement):
            if 'texture' in element.element:
                CopyFiles(MakePath('assets', 'textures', 'ui'), MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures', 'ui'), f"{element.element['texture'].split('/')[-1]}.png")
            for elem in element._controls:
                copy_textures(elem)

        for element in self._elements:
            copy_textures(element)
            self._content.update(element.queue)
        return super().queue(directory)


class UI():
    class _HUDScreen(_UIScreen):
        def __init__(self, anvil_animation: _UIAnimation, variables: _UIVariables) -> None:
            super().__init__('hud_screen', 'hud', anvil_animation, variables)
            #Disable HUD
            root_panel = self.add_element('root_panel')
            root_panel.binding.binding_name('#hud_title_text_string').binding_name_override('#text')
            root_panel.binding.binding_type(UIBindingType.View).source_property_name('$anvil.hud_visible').target_property_name('#visible')

            hud_title_text = self.add_element('hud_title_text')
            hud_title_text.binding.binding_name('#hud_title_text_string').binding_name_override('#text')
            hud_title_text.binding.binding_name('#hud_subtitle_text_string').binding_name_override('#subtext')
            hud_title_text.binding.binding_type(UIBindingType.View).source_property_name('$anvil.title.bool').target_property_name('#visible')
            
            hud_actionbar_text = self.add_element('hud_actionbar_text')
            hud_actionbar_text.visible('$anvil.actionbar.bool')
            hud_actionbar_text.keys('text', '$actionbar_text')

            anvil_element = self.add_element('hud_content')
            # TO DO:
            # Add a modifications controlling class
            anvil_element.binding.binding_name('#hud_visible').binding_name_override('#visible').binding_type(UIBindingType.Global)
            anvil_element.element.update({
                "modifications": [
                    {
                        "array_name": "controls",
                        "operation": "insert_front",
                        "value": {
                            "@anvil_hud.test_hud": {
                                "visible": True
                            }
                        }
                    }
                ]
            })
            variables.add_variable('$anvil.show.text', f'{NAMESPACE}:show')
            variables.add_variable('$anvil.hide.text', f'{NAMESPACE}:hide')
            self._ignored_title_texts = ['(#text = $anvil.show.text)', '(#text = $anvil.hide.text)']
            self._ignored_actionbar_texts = []

        def disable_mouse(self):
            self.add_element('hud_screen@common.base_screen').should_steal_mouse.absorbs_input
            self.add_element('cursor_renderer').visible(False)
            return self
    
    class _AnvilScreen(_UIScreen):
        def __init__(self, anvil_animation: _UIAnimation, variables: _UIVariables) -> None:
            super().__init__('hud', 'anvil_hud', anvil_animation, variables)
            self.test_hud = self.add_element('test_hud')
            self.test_hud.type(UIElementType.Panel)

        def add_element(self, element_name: str, trigger: UIElementTrigger = UIElementTrigger.NONE, keyword: str = None):
            if trigger is not None:
                self.test_hud.controls(f'{element_name}@anvil_hud.{element_name}_factory').visible(True)

            return super().add_element(element_name, trigger, keyword)
        
        # Layer 100
        def add_logo(self):
            #animations
            logo_zoom = self._anvil_animation.add_animation('logo_zoom')
            logo_zoom.anim_type(UIAnimType.Size)
            logo_zoom.easing(UIEasing.Linear)
            logo_zoom.from_(("38%", "38%")).to(("71%", "71%"))
            logo_zoom.duration('$anvil.logo.logo_zoom')
            self._variables.add_variable('$anvil.logo.logo_zoom', 13.7)
            logo_zoom.destroy_at_end('@anvil_hud.logo_element')

            logo_alpha_in = self._anvil_animation.add_animation('logo_alpha_in')
            logo_alpha_in.anim_type(UIAnimType.Alpha)
            logo_alpha_in.easing(UIEasing.OutQuad)
            logo_alpha_in.from_(0)
            logo_alpha_in.to(1)
            logo_alpha_in.duration('$title_fade_in_time')
            logo_alpha_in.next('@anvil_animations.logo_alpha_wait')

            logo_alpha_wait = self._anvil_animation.add_animation('logo_alpha_wait')
            logo_alpha_wait.anim_type(UIAnimType.Wait)
            logo_alpha_wait.duration('$title_stay_time')
            logo_alpha_wait.next('@anvil_animations.logo_alpha_out')

            logo_alpha_out = self._anvil_animation.add_animation('logo_alpha_out')
            logo_alpha_out.anim_type(UIAnimType.Alpha)
            logo_alpha_out.easing(UIEasing.InOutSine)
            logo_alpha_out.from_(1)
            logo_alpha_out.to(0)
            logo_alpha_out.duration('$title_fade_out_time')

            #element
            logo_element = self.add_element('logo_element', UIElementTrigger.Title, 'logo')
            logo_element.type(UIElementType.Image)
            logo_element.layer(100)
            logo_element.texture('logo')
            logo_element.anchor(UIAnchor.Center, UIAnchor.Center)
            logo_element.binding.binding_name('#hud_title_text_string').binding_name_override('#text')
            logo_element.binding.binding_type(UIBindingType.View).source_property_name('$anvil.logo_element.bool').target_property_name('#visible')
            logo_element.size('@anvil_animations.logo_zoom')
            logo_element.alpha('@anvil_animations.logo_alpha_in')
        # Layer 101
        def add_blinking_screen(self):
            # animation
            blink_fade_in = self._anvil_animation.add_animation('blink_fade_in')
            blink_fade_in.anim_type(UIAnimType.Alpha)
            blink_fade_in.easing(UIEasing.InOutSine)
            blink_fade_in.from_(0).to(1)
            self._variables.add_variable('$anvil.blink.fade_in', 1)
            blink_fade_in.duration('$anvil.blink.fade_in')
            blink_fade_in.next('@anvil_animations.blink_fade_stay')

            blink_fade_stay = self._anvil_animation.add_animation('blink_fade_stay')
            blink_fade_stay.anim_type(UIAnimType.Wait)
            self._variables.add_variable('$anvil.blink.fade_stay', 1)
            blink_fade_stay.duration('$anvil.blink.fade_stay')
            blink_fade_stay.next('@anvil_animations.blink_fade_out')

            blink_fade_out = self._anvil_animation.add_animation('blink_fade_out')
            blink_fade_out.anim_type(UIAnimType.Alpha)
            blink_fade_out.easing(UIEasing.InOutSine)
            blink_fade_out.from_(1).to(0)
            self._variables.add_variable('$anvil.blink.fade_out', 1)
            blink_fade_out.duration('$anvil.blink.fade_out')
            blink_fade_out.destroy_at_end('@anvil_hud.blink_element')
            # element
            blink_element = self.add_element('blink_element', UIElementTrigger.Title, 'blink')
            blink_element.type(UIElementType.Image)
            blink_element.layer(101)
            blink_element.texture('black_element')
            blink_element.anchor(UIAnchor.Center, UIAnchor.Center)
            blink_element.size(('300%', '300%'))
            blink_element.alpha('@anvil_animations.blink_fade_in')
            blink_element.binding.binding_name('#hud_title_text_string').binding_name_override('#text')
            blink_element.binding.binding_type(UIBindingType.View).source_property_name('$anvil.blink_element.bool').target_property_name('#visible')
        # Layer 101
        def add_black_bars(self):
            black_bars_in = self._anvil_animation.add_animation('black_bars_in')
            black_bars_in.anim_type(UIAnimType.Size)
            black_bars_in.easing(UIEasing.InOutSine)
            black_bars_in.from_(('300%', '300%')).to(('300%', '100%'))
            self._variables.add_variable('$anvil.black_bars.in', 1.6)
            black_bars_in.duration('$anvil.black_bars.in')
            black_bars_in.next('@anvil_animations.black_bars_wait')

            black_bars_wait = self._anvil_animation.add_animation('black_bars_wait')
            black_bars_wait.anim_type(UIAnimType.Wait)
            self._variables.add_variable('$anvil.black_bars.stay', 1)
            black_bars_wait.duration('$anvil.black_bars.stay')
            
            black_bars_out = self._anvil_animation.add_animation('black_bars_out')
            black_bars_out.anim_type(UIAnimType.Size)
            black_bars_out.easing(UIEasing.InOutSine)
            black_bars_out.from_(('300%', '100%')).to(('300%', '300%'))
            self._variables.add_variable('$anvil.black_bars.out', 1.6)
            black_bars_out.duration('$anvil.black_bars.out')
            black_bars_out.destroy_at_end('@anvil_hud.black_bars_element')

            # element
            black_bars = self.add_element('black_bars_element', UIElementTrigger.Actionbar)
            black_bars.type(UIElementType.Image)
            black_bars.texture('black_bars')
            black_bars.keep_ratio(False)
            black_bars.anchor(UIAnchor.Center, UIAnchor.Center)
            black_bars.layer(101)
            black_bars.keys('anim_size', ('300%', '300%'))
            black_bars.keys('text', '$actionbar_text')
            black_bars.variables('$anvil.black_bars_in.bool', 'anim_size', '@anvil_animations.black_bars_in')
            black_bars.variables('$anvil.black_bars_out.bool', 'anim_size', '@anvil_animations.black_bars_out')
            black_bars.size('$anim_size')

            self._variables.add_variable(f'$anvil.black_bars_in.text', f'{NAMESPACE}:bars_in')
            self._variables.add_variable(f'$anvil.black_bars_in.bool', f'($text = $anvil.black_bars_in.text)')
            self._variables.add_variable(f'$anvil.black_bars_out.text', f'{NAMESPACE}:bars_out')
            self._variables.add_variable(f'$anvil.black_bars_out.bool', f'($text = $anvil.black_bars_out.text)')

            self._ignored_actionbar_texts.extend(['($text = $anvil.black_bars_in.text)', '($text = $anvil.black_bars_out.text)'])
        # Layer 101
        def add_scope_view(self):
            self._variables.add_variable('$anvil.scope_view_in.duration', 1.6)
            self._variables.add_variable('$anvil.scope_view_out.duration', 1.6)

            self._variables.add_variable('$anvil.scope_view_in.text', f'{NAMESPACE}:scope_view_in')
            self._variables.add_variable('$anvil.scope_view_in.bool', '($text = $anvil.scope_view_in.text)')
            self._variables.add_variable('$anvil.scope_view_out.text', f'{NAMESPACE}:scope_view_out')
            self._variables.add_variable('$anvil.scope_view_out.bool', '($text = $anvil.scope_view_out.text)')

            self._variables.add_variable('$anvil.scope_view_full_in.text', f'{NAMESPACE}:scope_view_full_in')
            self._variables.add_variable('$anvil.scope_view_full_in.bool', '($text = $anvil.scope_view_full_in.text)')
            self._variables.add_variable('$anvil.scope_view_full_out.text', f'{NAMESPACE}:scope_view_full_out')
            self._variables.add_variable('$anvil.scope_view_full_out.bool', '($text = $anvil.scope_view_full_out.text)')

            scope_view_in = self._anvil_animation.add_animation('scope_view_in')
            scope_view_in.anim_type(UIAnimType.Size)\
                .easing(UIEasing.InOutSine)\
                .from_(('100%y', '300%')).to(('100%y', '40%'))\
                .duration('$anvil.scope_view_in.duration')\
                .next('@anvil_animations.scope_view_wait')
            scope_view_wait = self._anvil_animation.add_animation('scope_view_wait')
            scope_view_wait.anim_type(UIAnimType.Wait)
            scope_view_out = self._anvil_animation.add_animation('scope_view_out')
            scope_view_out.anim_type(UIAnimType.Size)\
                .easing(UIEasing.InOutSine)\
                .from_(('100%y', '40%')).to(('100%y', '300%'))\
                .duration('$anvil.scope_view_out.duration')\
                .destroy_at_end('@anvil_hud.scope_view')

            scope_view_full_in = self._anvil_animation.add_animation('scope_view_full_in')
            scope_view_full_in.anim_type(UIAnimType.Size)\
                .easing(UIEasing.InOutSine)\
                .from_(('100%y', '300%')).to(('100%y', '0.3%'))\
                .duration('$anvil.scope_view_in.duration')\
                .next('@anvil_animations.scope_view_full_wait')
            scope_view_full_wait = self._anvil_animation.add_animation('scope_view_full_wait')
            scope_view_full_wait.anim_type(UIAnimType.Wait)
            scope_view_full_out = self._anvil_animation.add_animation('scope_view_full_out')
            scope_view_full_out.anim_type(UIAnimType.Size)\
                .easing(UIEasing.InOutSine)\
                .from_(('100%y', '0.3%')).to(('100%y', '300%'))\
                .duration('$anvil.scope_view_out.duration')\
                .destroy_at_end('@anvil_hud.scope_view')

            # element
            scope_view = self.add_element('scope_view', UIElementTrigger.Actionbar)
            scope_view.type(UIElementType.Image)\
                .offset((0,"10px"))\
                .texture('scope_view')\
                .keep_ratio(False)\
                .anchor(UIAnchor.Center, UIAnchor.Center)\
                .layer(101)\
                .keys('anim_size', ("300%","300%"))\
                .keys('text', '$actionbar_text')\
                .variables('$anvil.scope_view_in.bool', 'anim_size', '@anvil_animations.scope_view_in')\
                .variables('$anvil.scope_view_out.bool', 'anim_size', '@anvil_animations.scope_view_out')\
                .variables('$anvil.scope_view_full_in.bool', 'anim_size', '@anvil_animations.scope_view_full_in')\
                .variables('$anvil.scope_view_full_out.bool', 'anim_size', '@anvil_animations.scope_view_full_out')\
                .size('$anim_size')\

            scope_view_right_bar = scope_view.controls('scope_view_right_bar')
            scope_view_right_bar.type(UIElementType.Image)\
                .texture('black_element')\
                .keep_ratio(False)\
                .anchor(UIAnchor.RightMiddle, UIAnchor.RightMiddle)\
                .size(('40000%', '40000%'))\
                .offset(('100%x', 0))
            scope_view_left_bar = scope_view.controls('scope_view_left_bar')
            scope_view_left_bar.type(UIElementType.Image)\
                .texture('black_element')\
                .keep_ratio(False)\
                .anchor(UIAnchor.LeftMiddle, UIAnchor.LeftMiddle)\
                .size(('40000%', '40000%'))\
                .offset(('-100%x', 0))
            scope_view_top_bar = scope_view.controls('scope_view_top_bar')
            scope_view_top_bar.type(UIElementType.Image)\
                .texture('black_element')\
                .keep_ratio(False)\
                .anchor(UIAnchor.TopMiddle, UIAnchor.TopMiddle)\
                .size(('40000%', '40000%'))\
                .offset((0, '-100%x'))
            scope_view_bottom_bar = scope_view.controls('scope_view_bottom_bar')
            scope_view_bottom_bar.type(UIElementType.Image)\
                .texture('black_element')\
                .keep_ratio(False)\
                .anchor(UIAnchor.BottomMiddle, UIAnchor.BottomMiddle)\
                .size(('40000%', '40000%'))\
                .offset((0, '100%x'))
        
            self._ignored_actionbar_texts.extend(['($text = $anvil.scope_view_in.text)', '($text = $anvil.scope_view_out.text)', '($text = $anvil.scope_view_full_in.text)', '($text = $anvil.scope_view_full_out.text)'])
        # Layer 102
        def add_info_card(self):
            info_in = self._anvil_animation.add_animation('info_in')
            info_in.anim_type(UIAnimType.Offset)
            info_in.easing(UIEasing.InOutSine)
            info_in.from_(("100%x","15%")).to((0,"15%"))
            self._variables.add_variable('$anvil.info.in', 0.5)
            info_in.duration('$anvil.info.in')
            info_in.next('@anvil_animations.info_wait')

            info_wait = self._anvil_animation.add_animation('info_wait')
            info_wait.anim_type(UIAnimType.Wait)
            self._variables.add_variable('$anvil.info.stay', 5)
            info_wait.duration('$anvil.info.stay')
            info_wait.next('@anvil_animations.info_out')

            info_out = self._anvil_animation.add_animation('info_out')
            info_out.anim_type(UIAnimType.Offset)
            info_out.easing(UIEasing.InOutSine)
            info_out.from_((0,"15%")).to(("100%x","15%"))
            self._variables.add_variable('$anvil.info.out', 0.5)
            info_out.duration('$anvil.info.out')
            info_in.destroy_at_end('@anvil_hud.info_card')

            # elements
            info_card = self.add_element('info_card', UIElementTrigger.Title, 'info')
            info_card.type(UIElementType.Image)
            info_card.layer(102)
            info_card.texture('info_card')
            info_card.size(("138px","32px"))
            info_card.anchor(UIAnchor.TopRight, UIAnchor.TopRight)
            info_card.offset('@anvil_animations.info_in')
            info_card.binding.binding_name('#hud_title_text_string').binding_name_override('#text')
            info_card.binding.binding_type(UIBindingType.View).source_property_name('$anvil.info_card.bool').target_property_name('#visible')
            info_text = info_card.controls('info_text')
            info_text.type(UIElementType.Label)
            info_text.size(("80%","90%"))
            info_text.offset(("4%","9%"))
            info_text.text_alignment(UIAnchor.Center)
            info_text.font_size(UIFontSize.Normal)
            info_text.shadow
            info_text.binding.binding_name('#hud_subtitle_text_string').binding_name_override('#text')
            info_text.text('#text')
        # Layer 103
        def add_loading_screen(self, load_time : int = 10):
            progress_bar_y_offset = 40
            progress_bar_height = 16
            text_y_offset = progress_bar_height + 5

            self._variables.add_variable('$anvil.loading_screen.in', 1)
            self._variables.add_variable('$anvil.loading_screen.stay', load_time)
            self._variables.add_variable('$anvil.loading_screen.out', 1)
            
            self._variables.add_variable('$anvil.loading_progress_bar.wait', 3)
            self._variables.add_variable('$anvil.loading_progress_bar.size', load_time-3)
            self._variables.add_variable('$anvil.loading_progress_bar.offset', load_time-3)

            
            loading_screen_alpha_in = self._anvil_animation.add_animation('loading_screen_alpha_in')
            loading_screen_alpha_wait = self._anvil_animation.add_animation('loading_screen_alpha_wait')
            loading_screen_alpha_out = self._anvil_animation.add_animation('loading_screen_alpha_out')

            loading_screen_alpha_in.anim_type(UIAnimType.Alpha)\
                .easing(UIEasing.Linear)\
                .from_(0).to(1)\
                .duration('$anvil.loading_screen.in')\
                .next('@anvil_animations.loading_screen_alpha_wait')
            loading_screen_alpha_wait.anim_type(UIAnimType.Wait)\
                .duration('$anvil.loading_screen.stay')\
                .next('@anvil_animations.loading_screen_alpha_out')
            loading_screen_alpha_out.anim_type(UIAnimType.Alpha)\
                .easing(UIEasing.Linear)\
                .from_(1).to(0)\
                .duration('$anvil.loading_screen.out')\
                .destroy_at_end('@anvil_hud.loading_screen')

            loading_progress_bar_size_in = self._anvil_animation.add_animation('loading_progress_bar_size_in')
            loading_progress_bar_size = self._anvil_animation.add_animation('loading_progress_bar_size')
            loading_progress_bar_offset_in = self._anvil_animation.add_animation('loading_progress_bar_offset_in')
            loading_progress_bar_offset = self._anvil_animation.add_animation('loading_progress_bar_offset')
            
            loading_progress_bar_size_in.anim_type(UIAnimType.Wait)\
                .from_((0,0))\
                .duration('$anvil.loading_progress_bar.wait')\
                .next('@anvil_animations.loading_progress_bar_size')
            loading_progress_bar_offset_in.anim_type(UIAnimType.Wait)\
                .duration('$anvil.loading_progress_bar.wait')\
                .next('@anvil_animations.loading_progress_bar_offset')
            loading_progress_bar_size.anim_type(UIAnimType.Size)\
                .easing(UIEasing.Linear)\
                .from_((0, f'{progress_bar_height/2}px')).to(('100%', f'{progress_bar_height/2}px'))\
                .duration('$anvil.loading_progress_bar.size')
            loading_progress_bar_offset.anim_type(UIAnimType.Offset)\
                .easing(UIEasing.Linear)\
                .from_(('-50%+1px', 0)).to((0, 0))\
                .duration('$anvil.loading_progress_bar.offset')

            # Loading Panel
            loading = self.add_element('loading_screen', UIElementTrigger.Title, 'loading')
            loading.binding.binding_name('#hud_title_text_string').binding_name_override('#text')
            loading.binding.binding_type(UIBindingType.View).source_property_name('$anvil.loading_screen.bool').target_property_name('#visible')
            loading.type(UIElementType.Image)\
                .layer(106)\
                .size(('100%', '100%'))\
                .alpha('@anvil_animations.loading_screen_alpha_in')\
                .anchor(UIAnchor.Center, UIAnchor.Center)\
                .propagate_alpha\
            
            # Loading Background
            loading_background = loading.controls('loading_bar')
            loading_background.type(UIElementType.Image)\
                .size(('100%', '100%x'))\
                .keep_ratio(True)\
                .texture('loading_background')\
            
            #Loading Bar
            loading_bar = loading.controls('loading_bar')
            loading_bar.type(UIElementType.Panel)\
                .size(('90%', f'{progress_bar_height}px'))\
                .offset((0, f'-{progress_bar_y_offset}px'))\
                .anchor(UIAnchor.BottomMiddle, UIAnchor.BottomMiddle)\

            # Loading text
            loading_text = loading_bar.controls('loading_text')
            loading_text.type(UIElementType.Label)\
                .anchor(UIAnchor.LeftMiddle, UIAnchor.LeftMiddle)\
                .offset((0, f'-{text_y_offset}px'))\
                .shadow\
                .font_size(UIFontSize.Large)\
                .text('Loading...')

            #Bar
            loading_progress_bar_background = loading_bar.controls('loading_progress_bar_background')
            loading_progress_bar_background.texture('loading_progress_bar_background')\
                .type(UIElementType.Image)\
                .keep_ratio(False)\
                .size(('100%', f'{progress_bar_height/2}px'))

            loading_progress_bar = loading_bar.controls('loading_progress_bar')
            loading_progress_bar.texture('loading_progress_bar')\
                .type(UIElementType.Image)\
                .keep_ratio(False)\
                .size('@anvil_animations.loading_progress_bar_size_in')\
                .offset('@anvil_animations.loading_progress_bar_offset_in')

            #loading_bar_middle = loading_bar.controls('loading_bar_middle')
            #loading_bar_middle.texture('loading_bar_outer')\
            #    .type(UIElementType.Image)\
            #    .uv((2, 0))\
            #    .uv_size((1, 8))\
            #    .keep_ratio(False)\
            #    .size(('100%', '100%'))
#
            #loading_bar_left = loading_bar.controls('loading_bar_left')
            #loading_bar_left.texture('loading_bar_outer')\
            #    .type(UIElementType.Image)\
            #    .anchor(UIAnchor.LeftMiddle, UIAnchor.LeftMiddle)\
            #    .uv((0, 0))\
            #    .uv_size((2, 8))\
            #    .keep_ratio(True)\
            #    .size(('4px', '100%'))
#
            #loading_bar_right = loading_bar.controls('loading_bar_right')
            #loading_bar_right.texture('loading_bar_outer')\
            #    .type(UIElementType.Image)\
            #    .anchor(UIAnchor.RightMiddle, UIAnchor.RightMiddle)\
            #    .uv((3, 0))\
            #    .uv_size((2, 8))\
            #    .keep_ratio(True)\
            #    .size(('4px', '100%'))


        def queue(self):
            return super().queue('anvil')

    class _AnvilAnimations(_UIAnimation):
        def __init__(self) -> None:
            super().__init__('animations', 'anvil_animations')

    def __init__(self) -> None:
        self.variables = _UIVariables()
        self._defs = Exporter('_ui_defs', 'uivars').content({'ui_defs': ['ui/anvil/animations.json','ui/anvil/hud.json',]})

        self.animations_screen = self._AnvilAnimations()
        self.hud_screen = self._HUDScreen(self.animations_screen, self.variables)
        self.anvil_screen = self._AnvilScreen(self.animations_screen, self.variables)

    def queue(self):
        # Manage Titles, Subtitles and actionbars
        ignored_title_texts = self.hud_screen._ignored_title_texts
        ignored_title_texts.extend(self.anvil_screen._ignored_title_texts)

        ignored_actionbar_texts = self.hud_screen._ignored_actionbar_texts
        ignored_actionbar_texts.extend(self.anvil_screen._ignored_actionbar_texts)
        
        #Manage Variables
        self.variables.add_variable('$anvil.title.bool', f'(not({" or ".join(ignored_title_texts)}))')
        self.variables.add_variable('$anvil.actionbar.bool', f'(not({" or ".join(ignored_actionbar_texts)}))')
        self.variables.add_variable('$anvil.hud_visible', f'({ignored_title_texts.pop(0)} or not ({ignored_title_texts.pop(0)}))')

        # Add to ANVIL queue
        self.hud_screen.queue()
        self.anvil_screen.queue()
        self.animations_screen.queue('anvil')
        self.variables.queue()
        self._defs.queue()
