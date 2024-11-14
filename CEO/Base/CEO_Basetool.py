from langchain.tools import BaseTool
"""Base implementation for tools or skills."""
# from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from inspect import signature
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple, Type, Union

from pydantic import (
    BaseModel,
    Extra,
    Field,
    create_model,
    root_validator,
    validate_arguments,
)
# from pydantic.main import ModelMetaclass

from langchain.callbacks.base import BaseCallbackManager
from langchain.callbacks.manager import (
    AsyncCallbackManager,
    AsyncCallbackManagerForToolRun,
    CallbackManager,
    CallbackManagerForToolRun,
    Callbacks,
)


class ToolException(Exception):
    """An optional exception that tool throws when execution error occurs.

    When this exception is thrown, the agent will not stop working,
    but will handle the exception according to the handle_tool_error
    variable of the tool, and the processing result will be returned
    to the agent as observation, and printed in red on the console.
    """

    pass
class CEOBaseTool(BaseTool):

    def run(
        self,
        tool_input: Union[str, Dict],
        verbose: Optional[bool] = None,
        start_color: Optional[str] = "green",
        color: Optional[str] = "green",
        callbacks: Callbacks = None,
        *,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run the tool."""
        parsed_input = self._parse_input(tool_input)
        if not self.verbose and verbose is not None:
            verbose_ = verbose
        else:
            verbose_ = self.verbose
        callback_manager = CallbackManager.configure(
            callbacks,
            self.callbacks,
            verbose_,
            tags,
            self.tags,
            metadata,
            self.metadata,
        )
        # TODO: maybe also pass through run_manager is _run supports kwargs
        new_arg_supported = signature(self._run).parameters.get("run_manager")
        run_manager = callback_manager.on_tool_start(
            {"name": self.name, "description": self.description},
            tool_input if isinstance(tool_input, str) else str(tool_input),
            color=start_color,
            **kwargs,
        )
        try:
            tool_args, tool_kwargs = self._to_args_and_kwargs(parsed_input)
            observation = (
                self._run(str(tool_kwargs))

            )
        except ToolException as e:
            if not self.handle_tool_error:
                run_manager.on_tool_error(e)
                raise e
            elif isinstance(self.handle_tool_error, bool):
                if e.args:
                    observation = e.args[0]
                else:
                    observation = "Tool execution error"
            elif isinstance(self.handle_tool_error, str):
                observation = self.handle_tool_error
            elif callable(self.handle_tool_error):
                observation = self.handle_tool_error(e)
            else:
                raise ValueError(
                    f"Got unexpected type of `handle_tool_error`. Expected bool, str "
                    f"or callable. Received: {self.handle_tool_error}"
                )
            run_manager.on_tool_end(
                str(observation), color="red", name=self.name, **kwargs
            )
            return observation
        except (Exception, KeyboardInterrupt) as e:
            run_manager.on_tool_error(e)
            raise e
        else:
            run_manager.on_tool_end(
                str(observation), color=color, name=self.name, **kwargs
            )
            return observation

    async def arun(
        self,
        tool_input: Union[str, Dict],
        verbose: Optional[bool] = None,
        start_color: Optional[str] = "green",
        color: Optional[str] = "green",
        callbacks: Callbacks = None,
        *,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run the tool asynchronously."""
        parsed_input = self._parse_input(tool_input)
        if not self.verbose and verbose is not None:
            verbose_ = verbose
        else:
            verbose_ = self.verbose
        callback_manager = AsyncCallbackManager.configure(
            callbacks,
            self.callbacks,
            verbose_,
            tags,
            self.tags,
            metadata,
            self.metadata,
        )
        new_arg_supported = signature(self._arun).parameters.get("run_manager")
        run_manager = await callback_manager.on_tool_start(
            {"name": self.name, "description": self.description},
            tool_input if isinstance(tool_input, str) else str(tool_input),
            color=start_color,
            **kwargs,
        )
        try:
            # We then call the tool on the tool input to get an observation
            tool_args, tool_kwargs = self._to_args_and_kwargs(parsed_input)
            observation = (
                await self._arun(*tool_args, run_manager=run_manager, **tool_kwargs)
                if new_arg_supported
                else await self._arun(*tool_args, **tool_kwargs)
            )
        except ToolException as e:
            if not self.handle_tool_error:
                await run_manager.on_tool_error(e)
                raise e
            elif isinstance(self.handle_tool_error, bool):
                if e.args:
                    observation = e.args[0]
                else:
                    observation = "Tool execution error"
            elif isinstance(self.handle_tool_error, str):
                observation = self.handle_tool_error
            elif callable(self.handle_tool_error):
                observation = self.handle_tool_error(e)
            else:
                raise ValueError(
                    f"Got unexpected type of `handle_tool_error`. Expected bool, str "
                    f"or callable. Received: {self.handle_tool_error}"
                )
            await run_manager.on_tool_end(
                str(observation), color="red", name=self.name, **kwargs
            )
            return observation
        except (Exception, KeyboardInterrupt) as e:
            await run_manager.on_tool_error(e)
            raise e
        else:
            await run_manager.on_tool_end(
                str(observation), color=color, name=self.name, **kwargs
            )
            return observation

    def __call__(self, tool_input: str, callbacks: Callbacks = None) -> str:
        """Make tool callable."""
        return self.run(tool_input, callbacks=callbacks)