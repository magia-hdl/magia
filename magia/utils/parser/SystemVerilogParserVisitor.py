# Generated from SystemVerilogParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .SystemVerilogParser import SystemVerilogParser
else:
    from SystemVerilogParser import SystemVerilogParser

# This class defines a complete generic visitor for a parse tree produced by SystemVerilogParser.

class SystemVerilogParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SystemVerilogParser#source_text.
    def visitSource_text(self, ctx:SystemVerilogParser.Source_textContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#description.
    def visitDescription(self, ctx:SystemVerilogParser.DescriptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#assignment_operator.
    def visitAssignment_operator(self, ctx:SystemVerilogParser.Assignment_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#edge_identifier.
    def visitEdge_identifier(self, ctx:SystemVerilogParser.Edge_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#identifier.
    def visitIdentifier(self, ctx:SystemVerilogParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#integer_type.
    def visitInteger_type(self, ctx:SystemVerilogParser.Integer_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#integer_atom_type.
    def visitInteger_atom_type(self, ctx:SystemVerilogParser.Integer_atom_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#integer_vector_type.
    def visitInteger_vector_type(self, ctx:SystemVerilogParser.Integer_vector_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#non_integer_type.
    def visitNon_integer_type(self, ctx:SystemVerilogParser.Non_integer_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#net_type.
    def visitNet_type(self, ctx:SystemVerilogParser.Net_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#unary_module_path_operator.
    def visitUnary_module_path_operator(self, ctx:SystemVerilogParser.Unary_module_path_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#unary_operator.
    def visitUnary_operator(self, ctx:SystemVerilogParser.Unary_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#inc_or_dec_operator.
    def visitInc_or_dec_operator(self, ctx:SystemVerilogParser.Inc_or_dec_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#implicit_class_handle.
    def visitImplicit_class_handle(self, ctx:SystemVerilogParser.Implicit_class_handleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#integral_number.
    def visitIntegral_number(self, ctx:SystemVerilogParser.Integral_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#real_number.
    def visitReal_number(self, ctx:SystemVerilogParser.Real_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#any_system_tf_identifier.
    def visitAny_system_tf_identifier(self, ctx:SystemVerilogParser.Any_system_tf_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#signing.
    def visitSigning(self, ctx:SystemVerilogParser.SigningContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#number.
    def visitNumber(self, ctx:SystemVerilogParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#timeunits_declaration.
    def visitTimeunits_declaration(self, ctx:SystemVerilogParser.Timeunits_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#lifetime.
    def visitLifetime(self, ctx:SystemVerilogParser.LifetimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#port_direction.
    def visitPort_direction(self, ctx:SystemVerilogParser.Port_directionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#always_keyword.
    def visitAlways_keyword(self, ctx:SystemVerilogParser.Always_keywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#join_keyword.
    def visitJoin_keyword(self, ctx:SystemVerilogParser.Join_keywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#unique_priority.
    def visitUnique_priority(self, ctx:SystemVerilogParser.Unique_priorityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#drive_strength.
    def visitDrive_strength(self, ctx:SystemVerilogParser.Drive_strengthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#strength0.
    def visitStrength0(self, ctx:SystemVerilogParser.Strength0Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#strength1.
    def visitStrength1(self, ctx:SystemVerilogParser.Strength1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#charge_strength.
    def visitCharge_strength(self, ctx:SystemVerilogParser.Charge_strengthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#sequence_lvar_port_direction.
    def visitSequence_lvar_port_direction(self, ctx:SystemVerilogParser.Sequence_lvar_port_directionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#bins_keyword.
    def visitBins_keyword(self, ctx:SystemVerilogParser.Bins_keywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#class_item_qualifier.
    def visitClass_item_qualifier(self, ctx:SystemVerilogParser.Class_item_qualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#random_qualifier.
    def visitRandom_qualifier(self, ctx:SystemVerilogParser.Random_qualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#property_qualifier.
    def visitProperty_qualifier(self, ctx:SystemVerilogParser.Property_qualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#method_qualifier.
    def visitMethod_qualifier(self, ctx:SystemVerilogParser.Method_qualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#constraint_prototype_qualifier.
    def visitConstraint_prototype_qualifier(self, ctx:SystemVerilogParser.Constraint_prototype_qualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#cmos_switchtype.
    def visitCmos_switchtype(self, ctx:SystemVerilogParser.Cmos_switchtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#enable_gatetype.
    def visitEnable_gatetype(self, ctx:SystemVerilogParser.Enable_gatetypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#mos_switchtype.
    def visitMos_switchtype(self, ctx:SystemVerilogParser.Mos_switchtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#n_input_gatetype.
    def visitN_input_gatetype(self, ctx:SystemVerilogParser.N_input_gatetypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#n_output_gatetype.
    def visitN_output_gatetype(self, ctx:SystemVerilogParser.N_output_gatetypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#pass_en_switchtype.
    def visitPass_en_switchtype(self, ctx:SystemVerilogParser.Pass_en_switchtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#pass_switchtype.
    def visitPass_switchtype(self, ctx:SystemVerilogParser.Pass_switchtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#any_implication.
    def visitAny_implication(self, ctx:SystemVerilogParser.Any_implicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#timing_check_event_control.
    def visitTiming_check_event_control(self, ctx:SystemVerilogParser.Timing_check_event_controlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#import_export.
    def visitImport_export(self, ctx:SystemVerilogParser.Import_exportContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#array_method_name.
    def visitArray_method_name(self, ctx:SystemVerilogParser.Array_method_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#operator_mul_div_mod.
    def visitOperator_mul_div_mod(self, ctx:SystemVerilogParser.Operator_mul_div_modContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#operator_plus_minus.
    def visitOperator_plus_minus(self, ctx:SystemVerilogParser.Operator_plus_minusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#operator_shift.
    def visitOperator_shift(self, ctx:SystemVerilogParser.Operator_shiftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#operator_cmp.
    def visitOperator_cmp(self, ctx:SystemVerilogParser.Operator_cmpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#operator_eq_neq.
    def visitOperator_eq_neq(self, ctx:SystemVerilogParser.Operator_eq_neqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#operator_xor.
    def visitOperator_xor(self, ctx:SystemVerilogParser.Operator_xorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#operator_impl.
    def visitOperator_impl(self, ctx:SystemVerilogParser.Operator_implContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#udp_nonansi_declaration.
    def visitUdp_nonansi_declaration(self, ctx:SystemVerilogParser.Udp_nonansi_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#udp_ansi_declaration.
    def visitUdp_ansi_declaration(self, ctx:SystemVerilogParser.Udp_ansi_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#udp_declaration.
    def visitUdp_declaration(self, ctx:SystemVerilogParser.Udp_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#udp_declaration_port_list.
    def visitUdp_declaration_port_list(self, ctx:SystemVerilogParser.Udp_declaration_port_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#udp_port_declaration.
    def visitUdp_port_declaration(self, ctx:SystemVerilogParser.Udp_port_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#udp_output_declaration.
    def visitUdp_output_declaration(self, ctx:SystemVerilogParser.Udp_output_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#udp_input_declaration.
    def visitUdp_input_declaration(self, ctx:SystemVerilogParser.Udp_input_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#udp_reg_declaration.
    def visitUdp_reg_declaration(self, ctx:SystemVerilogParser.Udp_reg_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#udp_body.
    def visitUdp_body(self, ctx:SystemVerilogParser.Udp_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#combinational_body.
    def visitCombinational_body(self, ctx:SystemVerilogParser.Combinational_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#combinational_entry.
    def visitCombinational_entry(self, ctx:SystemVerilogParser.Combinational_entryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#sequential_body.
    def visitSequential_body(self, ctx:SystemVerilogParser.Sequential_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#udp_initial_statement.
    def visitUdp_initial_statement(self, ctx:SystemVerilogParser.Udp_initial_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#sequential_entry.
    def visitSequential_entry(self, ctx:SystemVerilogParser.Sequential_entryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#seq_input_list.
    def visitSeq_input_list(self, ctx:SystemVerilogParser.Seq_input_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#level_input_list.
    def visitLevel_input_list(self, ctx:SystemVerilogParser.Level_input_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#edge_input_list.
    def visitEdge_input_list(self, ctx:SystemVerilogParser.Edge_input_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#edge_indicator.
    def visitEdge_indicator(self, ctx:SystemVerilogParser.Edge_indicatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#current_state.
    def visitCurrent_state(self, ctx:SystemVerilogParser.Current_stateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#next_state.
    def visitNext_state(self, ctx:SystemVerilogParser.Next_stateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#interface_declaration.
    def visitInterface_declaration(self, ctx:SystemVerilogParser.Interface_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#interface_header.
    def visitInterface_header(self, ctx:SystemVerilogParser.Interface_headerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#interface_item.
    def visitInterface_item(self, ctx:SystemVerilogParser.Interface_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#modport_declaration.
    def visitModport_declaration(self, ctx:SystemVerilogParser.Modport_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#modport_item.
    def visitModport_item(self, ctx:SystemVerilogParser.Modport_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#modport_ports_declaration.
    def visitModport_ports_declaration(self, ctx:SystemVerilogParser.Modport_ports_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#modport_clocking_declaration.
    def visitModport_clocking_declaration(self, ctx:SystemVerilogParser.Modport_clocking_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#modport_simple_ports_declaration.
    def visitModport_simple_ports_declaration(self, ctx:SystemVerilogParser.Modport_simple_ports_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#modport_simple_port.
    def visitModport_simple_port(self, ctx:SystemVerilogParser.Modport_simple_portContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#modport_tf_ports_declaration.
    def visitModport_tf_ports_declaration(self, ctx:SystemVerilogParser.Modport_tf_ports_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#modport_tf_port.
    def visitModport_tf_port(self, ctx:SystemVerilogParser.Modport_tf_portContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#statement_or_null.
    def visitStatement_or_null(self, ctx:SystemVerilogParser.Statement_or_nullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#initial_construct.
    def visitInitial_construct(self, ctx:SystemVerilogParser.Initial_constructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#default_clocking_or_dissable_construct.
    def visitDefault_clocking_or_dissable_construct(self, ctx:SystemVerilogParser.Default_clocking_or_dissable_constructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#statement.
    def visitStatement(self, ctx:SystemVerilogParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#statement_item.
    def visitStatement_item(self, ctx:SystemVerilogParser.Statement_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#cycle_delay.
    def visitCycle_delay(self, ctx:SystemVerilogParser.Cycle_delayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#clocking_drive.
    def visitClocking_drive(self, ctx:SystemVerilogParser.Clocking_driveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#clockvar_expression.
    def visitClockvar_expression(self, ctx:SystemVerilogParser.Clockvar_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#final_construct.
    def visitFinal_construct(self, ctx:SystemVerilogParser.Final_constructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#blocking_assignment.
    def visitBlocking_assignment(self, ctx:SystemVerilogParser.Blocking_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#procedural_timing_control_statement.
    def visitProcedural_timing_control_statement(self, ctx:SystemVerilogParser.Procedural_timing_control_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#procedural_timing_control.
    def visitProcedural_timing_control(self, ctx:SystemVerilogParser.Procedural_timing_controlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#event_control.
    def visitEvent_control(self, ctx:SystemVerilogParser.Event_controlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#delay_or_event_control.
    def visitDelay_or_event_control(self, ctx:SystemVerilogParser.Delay_or_event_controlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#delay3.
    def visitDelay3(self, ctx:SystemVerilogParser.Delay3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#delay2.
    def visitDelay2(self, ctx:SystemVerilogParser.Delay2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#delay_value.
    def visitDelay_value(self, ctx:SystemVerilogParser.Delay_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#delay_control.
    def visitDelay_control(self, ctx:SystemVerilogParser.Delay_controlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#nonblocking_assignment.
    def visitNonblocking_assignment(self, ctx:SystemVerilogParser.Nonblocking_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#procedural_continuous_assignment.
    def visitProcedural_continuous_assignment(self, ctx:SystemVerilogParser.Procedural_continuous_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#variable_assignment.
    def visitVariable_assignment(self, ctx:SystemVerilogParser.Variable_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#action_block.
    def visitAction_block(self, ctx:SystemVerilogParser.Action_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#seq_block.
    def visitSeq_block(self, ctx:SystemVerilogParser.Seq_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#par_block.
    def visitPar_block(self, ctx:SystemVerilogParser.Par_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#case_statement.
    def visitCase_statement(self, ctx:SystemVerilogParser.Case_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#case_keyword.
    def visitCase_keyword(self, ctx:SystemVerilogParser.Case_keywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#case_item.
    def visitCase_item(self, ctx:SystemVerilogParser.Case_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#case_pattern_item.
    def visitCase_pattern_item(self, ctx:SystemVerilogParser.Case_pattern_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#case_inside_item.
    def visitCase_inside_item(self, ctx:SystemVerilogParser.Case_inside_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#randcase_statement.
    def visitRandcase_statement(self, ctx:SystemVerilogParser.Randcase_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#randcase_item.
    def visitRandcase_item(self, ctx:SystemVerilogParser.Randcase_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#cond_predicate.
    def visitCond_predicate(self, ctx:SystemVerilogParser.Cond_predicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#conditional_statement.
    def visitConditional_statement(self, ctx:SystemVerilogParser.Conditional_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#subroutine_call_statement.
    def visitSubroutine_call_statement(self, ctx:SystemVerilogParser.Subroutine_call_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#disable_statement.
    def visitDisable_statement(self, ctx:SystemVerilogParser.Disable_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#event_trigger.
    def visitEvent_trigger(self, ctx:SystemVerilogParser.Event_triggerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#loop_statement.
    def visitLoop_statement(self, ctx:SystemVerilogParser.Loop_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_variable_assignments.
    def visitList_of_variable_assignments(self, ctx:SystemVerilogParser.List_of_variable_assignmentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#for_initialization.
    def visitFor_initialization(self, ctx:SystemVerilogParser.For_initializationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#for_variable_declaration_var_assign.
    def visitFor_variable_declaration_var_assign(self, ctx:SystemVerilogParser.For_variable_declaration_var_assignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#for_variable_declaration.
    def visitFor_variable_declaration(self, ctx:SystemVerilogParser.For_variable_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#for_step.
    def visitFor_step(self, ctx:SystemVerilogParser.For_stepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#loop_variables.
    def visitLoop_variables(self, ctx:SystemVerilogParser.Loop_variablesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#jump_statement.
    def visitJump_statement(self, ctx:SystemVerilogParser.Jump_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#wait_statement.
    def visitWait_statement(self, ctx:SystemVerilogParser.Wait_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#name_of_instance.
    def visitName_of_instance(self, ctx:SystemVerilogParser.Name_of_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#checker_instantiation.
    def visitChecker_instantiation(self, ctx:SystemVerilogParser.Checker_instantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_checker_port_connections.
    def visitList_of_checker_port_connections(self, ctx:SystemVerilogParser.List_of_checker_port_connectionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#ordered_checker_port_connection.
    def visitOrdered_checker_port_connection(self, ctx:SystemVerilogParser.Ordered_checker_port_connectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#named_checker_port_connection.
    def visitNamed_checker_port_connection(self, ctx:SystemVerilogParser.Named_checker_port_connectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#procedural_assertion_statement.
    def visitProcedural_assertion_statement(self, ctx:SystemVerilogParser.Procedural_assertion_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#concurrent_assertion_statement.
    def visitConcurrent_assertion_statement(self, ctx:SystemVerilogParser.Concurrent_assertion_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#assertion_item.
    def visitAssertion_item(self, ctx:SystemVerilogParser.Assertion_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#concurrent_assertion_item.
    def visitConcurrent_assertion_item(self, ctx:SystemVerilogParser.Concurrent_assertion_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#immediate_assertion_statement.
    def visitImmediate_assertion_statement(self, ctx:SystemVerilogParser.Immediate_assertion_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#simple_immediate_assertion_statement.
    def visitSimple_immediate_assertion_statement(self, ctx:SystemVerilogParser.Simple_immediate_assertion_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#simple_immediate_assert_statement.
    def visitSimple_immediate_assert_statement(self, ctx:SystemVerilogParser.Simple_immediate_assert_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#simple_immediate_assume_statement.
    def visitSimple_immediate_assume_statement(self, ctx:SystemVerilogParser.Simple_immediate_assume_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#simple_immediate_cover_statement.
    def visitSimple_immediate_cover_statement(self, ctx:SystemVerilogParser.Simple_immediate_cover_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#deferred_immediate_assertion_statement.
    def visitDeferred_immediate_assertion_statement(self, ctx:SystemVerilogParser.Deferred_immediate_assertion_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#primitive_delay.
    def visitPrimitive_delay(self, ctx:SystemVerilogParser.Primitive_delayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#deferred_immediate_assert_statement.
    def visitDeferred_immediate_assert_statement(self, ctx:SystemVerilogParser.Deferred_immediate_assert_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#deferred_immediate_assume_statement.
    def visitDeferred_immediate_assume_statement(self, ctx:SystemVerilogParser.Deferred_immediate_assume_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#deferred_immediate_cover_statement.
    def visitDeferred_immediate_cover_statement(self, ctx:SystemVerilogParser.Deferred_immediate_cover_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#weight_specification.
    def visitWeight_specification(self, ctx:SystemVerilogParser.Weight_specificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#production_item.
    def visitProduction_item(self, ctx:SystemVerilogParser.Production_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#rs_code_block.
    def visitRs_code_block(self, ctx:SystemVerilogParser.Rs_code_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#randsequence_statement.
    def visitRandsequence_statement(self, ctx:SystemVerilogParser.Randsequence_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#rs_prod.
    def visitRs_prod(self, ctx:SystemVerilogParser.Rs_prodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#rs_if_else.
    def visitRs_if_else(self, ctx:SystemVerilogParser.Rs_if_elseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#rs_repeat.
    def visitRs_repeat(self, ctx:SystemVerilogParser.Rs_repeatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#rs_case.
    def visitRs_case(self, ctx:SystemVerilogParser.Rs_caseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#rs_case_item.
    def visitRs_case_item(self, ctx:SystemVerilogParser.Rs_case_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#rs_rule.
    def visitRs_rule(self, ctx:SystemVerilogParser.Rs_ruleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#rs_production_list.
    def visitRs_production_list(self, ctx:SystemVerilogParser.Rs_production_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#production.
    def visitProduction(self, ctx:SystemVerilogParser.ProductionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#tf_item_declaration.
    def visitTf_item_declaration(self, ctx:SystemVerilogParser.Tf_item_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#tf_port_list.
    def visitTf_port_list(self, ctx:SystemVerilogParser.Tf_port_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#tf_port_item.
    def visitTf_port_item(self, ctx:SystemVerilogParser.Tf_port_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#tf_port_direction.
    def visitTf_port_direction(self, ctx:SystemVerilogParser.Tf_port_directionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#tf_port_declaration.
    def visitTf_port_declaration(self, ctx:SystemVerilogParser.Tf_port_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_tf_variable_identifiers_item.
    def visitList_of_tf_variable_identifiers_item(self, ctx:SystemVerilogParser.List_of_tf_variable_identifiers_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_tf_variable_identifiers.
    def visitList_of_tf_variable_identifiers(self, ctx:SystemVerilogParser.List_of_tf_variable_identifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#expect_property_statement.
    def visitExpect_property_statement(self, ctx:SystemVerilogParser.Expect_property_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#block_item_declaration.
    def visitBlock_item_declaration(self, ctx:SystemVerilogParser.Block_item_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#param_assignment.
    def visitParam_assignment(self, ctx:SystemVerilogParser.Param_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#type_assignment.
    def visitType_assignment(self, ctx:SystemVerilogParser.Type_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_type_assignments.
    def visitList_of_type_assignments(self, ctx:SystemVerilogParser.List_of_type_assignmentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_param_assignments.
    def visitList_of_param_assignments(self, ctx:SystemVerilogParser.List_of_param_assignmentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#local_parameter_declaration.
    def visitLocal_parameter_declaration(self, ctx:SystemVerilogParser.Local_parameter_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#parameter_declaration.
    def visitParameter_declaration(self, ctx:SystemVerilogParser.Parameter_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#type_declaration.
    def visitType_declaration(self, ctx:SystemVerilogParser.Type_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#net_type_declaration.
    def visitNet_type_declaration(self, ctx:SystemVerilogParser.Net_type_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#let_declaration.
    def visitLet_declaration(self, ctx:SystemVerilogParser.Let_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#let_port_list.
    def visitLet_port_list(self, ctx:SystemVerilogParser.Let_port_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#let_port_item.
    def visitLet_port_item(self, ctx:SystemVerilogParser.Let_port_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#let_formal_type.
    def visitLet_formal_type(self, ctx:SystemVerilogParser.Let_formal_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#package_import_declaration.
    def visitPackage_import_declaration(self, ctx:SystemVerilogParser.Package_import_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#package_import_item.
    def visitPackage_import_item(self, ctx:SystemVerilogParser.Package_import_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#property_list_of_arguments.
    def visitProperty_list_of_arguments(self, ctx:SystemVerilogParser.Property_list_of_argumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#property_actual_arg.
    def visitProperty_actual_arg(self, ctx:SystemVerilogParser.Property_actual_argContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#property_formal_type.
    def visitProperty_formal_type(self, ctx:SystemVerilogParser.Property_formal_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#sequence_formal_type.
    def visitSequence_formal_type(self, ctx:SystemVerilogParser.Sequence_formal_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#property_instance.
    def visitProperty_instance(self, ctx:SystemVerilogParser.Property_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#property_spec.
    def visitProperty_spec(self, ctx:SystemVerilogParser.Property_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#property_expr.
    def visitProperty_expr(self, ctx:SystemVerilogParser.Property_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#property_case_item.
    def visitProperty_case_item(self, ctx:SystemVerilogParser.Property_case_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#bit_select.
    def visitBit_select(self, ctx:SystemVerilogParser.Bit_selectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#identifier_with_bit_select.
    def visitIdentifier_with_bit_select(self, ctx:SystemVerilogParser.Identifier_with_bit_selectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#package_or_class_scoped_hier_id_with_select.
    def visitPackage_or_class_scoped_hier_id_with_select(self, ctx:SystemVerilogParser.Package_or_class_scoped_hier_id_with_selectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#package_or_class_scoped_path_item.
    def visitPackage_or_class_scoped_path_item(self, ctx:SystemVerilogParser.Package_or_class_scoped_path_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#package_or_class_scoped_path.
    def visitPackage_or_class_scoped_path(self, ctx:SystemVerilogParser.Package_or_class_scoped_pathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#hierarchical_identifier.
    def visitHierarchical_identifier(self, ctx:SystemVerilogParser.Hierarchical_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#package_or_class_scoped_id.
    def visitPackage_or_class_scoped_id(self, ctx:SystemVerilogParser.Package_or_class_scoped_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#select.
    def visitSelect(self, ctx:SystemVerilogParser.SelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#event_expression_item.
    def visitEvent_expression_item(self, ctx:SystemVerilogParser.Event_expression_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#event_expression.
    def visitEvent_expression(self, ctx:SystemVerilogParser.Event_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#boolean_abbrev.
    def visitBoolean_abbrev(self, ctx:SystemVerilogParser.Boolean_abbrevContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#sequence_abbrev.
    def visitSequence_abbrev(self, ctx:SystemVerilogParser.Sequence_abbrevContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#consecutive_repetition.
    def visitConsecutive_repetition(self, ctx:SystemVerilogParser.Consecutive_repetitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#non_consecutive_repetition.
    def visitNon_consecutive_repetition(self, ctx:SystemVerilogParser.Non_consecutive_repetitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#goto_repetition.
    def visitGoto_repetition(self, ctx:SystemVerilogParser.Goto_repetitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#cycle_delay_const_range_expression.
    def visitCycle_delay_const_range_expression(self, ctx:SystemVerilogParser.Cycle_delay_const_range_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#sequence_instance.
    def visitSequence_instance(self, ctx:SystemVerilogParser.Sequence_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#sequence_expr.
    def visitSequence_expr(self, ctx:SystemVerilogParser.Sequence_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#sequence_match_item.
    def visitSequence_match_item(self, ctx:SystemVerilogParser.Sequence_match_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#operator_assignment.
    def visitOperator_assignment(self, ctx:SystemVerilogParser.Operator_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#sequence_actual_arg.
    def visitSequence_actual_arg(self, ctx:SystemVerilogParser.Sequence_actual_argContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dist_weight.
    def visitDist_weight(self, ctx:SystemVerilogParser.Dist_weightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#clocking_declaration.
    def visitClocking_declaration(self, ctx:SystemVerilogParser.Clocking_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#clocking_item.
    def visitClocking_item(self, ctx:SystemVerilogParser.Clocking_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_clocking_decl_assign.
    def visitList_of_clocking_decl_assign(self, ctx:SystemVerilogParser.List_of_clocking_decl_assignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#clocking_decl_assign.
    def visitClocking_decl_assign(self, ctx:SystemVerilogParser.Clocking_decl_assignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#default_skew.
    def visitDefault_skew(self, ctx:SystemVerilogParser.Default_skewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#clocking_direction.
    def visitClocking_direction(self, ctx:SystemVerilogParser.Clocking_directionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#clocking_skew.
    def visitClocking_skew(self, ctx:SystemVerilogParser.Clocking_skewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#clocking_event.
    def visitClocking_event(self, ctx:SystemVerilogParser.Clocking_eventContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#cycle_delay_range.
    def visitCycle_delay_range(self, ctx:SystemVerilogParser.Cycle_delay_rangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#expression_or_dist.
    def visitExpression_or_dist(self, ctx:SystemVerilogParser.Expression_or_distContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#covergroup_declaration.
    def visitCovergroup_declaration(self, ctx:SystemVerilogParser.Covergroup_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#cover_cross.
    def visitCover_cross(self, ctx:SystemVerilogParser.Cover_crossContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#identifier_list_2plus.
    def visitIdentifier_list_2plus(self, ctx:SystemVerilogParser.Identifier_list_2plusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#cross_body.
    def visitCross_body(self, ctx:SystemVerilogParser.Cross_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#cross_body_item.
    def visitCross_body_item(self, ctx:SystemVerilogParser.Cross_body_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#bins_selection_or_option.
    def visitBins_selection_or_option(self, ctx:SystemVerilogParser.Bins_selection_or_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#bins_selection.
    def visitBins_selection(self, ctx:SystemVerilogParser.Bins_selectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#select_expression.
    def visitSelect_expression(self, ctx:SystemVerilogParser.Select_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#select_condition.
    def visitSelect_condition(self, ctx:SystemVerilogParser.Select_conditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#bins_expression.
    def visitBins_expression(self, ctx:SystemVerilogParser.Bins_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#covergroup_range_list.
    def visitCovergroup_range_list(self, ctx:SystemVerilogParser.Covergroup_range_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#covergroup_value_range.
    def visitCovergroup_value_range(self, ctx:SystemVerilogParser.Covergroup_value_rangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#covergroup_expression.
    def visitCovergroup_expression(self, ctx:SystemVerilogParser.Covergroup_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#coverage_spec_or_option.
    def visitCoverage_spec_or_option(self, ctx:SystemVerilogParser.Coverage_spec_or_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#coverage_option.
    def visitCoverage_option(self, ctx:SystemVerilogParser.Coverage_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#coverage_spec.
    def visitCoverage_spec(self, ctx:SystemVerilogParser.Coverage_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#cover_point.
    def visitCover_point(self, ctx:SystemVerilogParser.Cover_pointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#bins_or_empty.
    def visitBins_or_empty(self, ctx:SystemVerilogParser.Bins_or_emptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#bins_or_options.
    def visitBins_or_options(self, ctx:SystemVerilogParser.Bins_or_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#trans_list.
    def visitTrans_list(self, ctx:SystemVerilogParser.Trans_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#trans_set.
    def visitTrans_set(self, ctx:SystemVerilogParser.Trans_setContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#trans_range_list.
    def visitTrans_range_list(self, ctx:SystemVerilogParser.Trans_range_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#repeat_range.
    def visitRepeat_range(self, ctx:SystemVerilogParser.Repeat_rangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#coverage_event.
    def visitCoverage_event(self, ctx:SystemVerilogParser.Coverage_eventContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#block_event_expression.
    def visitBlock_event_expression(self, ctx:SystemVerilogParser.Block_event_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#hierarchical_btf_identifier.
    def visitHierarchical_btf_identifier(self, ctx:SystemVerilogParser.Hierarchical_btf_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#assertion_variable_declaration.
    def visitAssertion_variable_declaration(self, ctx:SystemVerilogParser.Assertion_variable_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dist_item.
    def visitDist_item(self, ctx:SystemVerilogParser.Dist_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#value_range.
    def visitValue_range(self, ctx:SystemVerilogParser.Value_rangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#attribute_instance.
    def visitAttribute_instance(self, ctx:SystemVerilogParser.Attribute_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#attr_spec.
    def visitAttr_spec(self, ctx:SystemVerilogParser.Attr_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#class_new.
    def visitClass_new(self, ctx:SystemVerilogParser.Class_newContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#param_expression.
    def visitParam_expression(self, ctx:SystemVerilogParser.Param_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#constant_param_expression.
    def visitConstant_param_expression(self, ctx:SystemVerilogParser.Constant_param_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#unpacked_dimension.
    def visitUnpacked_dimension(self, ctx:SystemVerilogParser.Unpacked_dimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#packed_dimension.
    def visitPacked_dimension(self, ctx:SystemVerilogParser.Packed_dimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#variable_dimension.
    def visitVariable_dimension(self, ctx:SystemVerilogParser.Variable_dimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#struct_union.
    def visitStruct_union(self, ctx:SystemVerilogParser.Struct_unionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#enum_base_type.
    def visitEnum_base_type(self, ctx:SystemVerilogParser.Enum_base_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#data_type_primitive.
    def visitData_type_primitive(self, ctx:SystemVerilogParser.Data_type_primitiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#data_type.
    def visitData_type(self, ctx:SystemVerilogParser.Data_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#data_type_or_implicit.
    def visitData_type_or_implicit(self, ctx:SystemVerilogParser.Data_type_or_implicitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#implicit_data_type.
    def visitImplicit_data_type(self, ctx:SystemVerilogParser.Implicit_data_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#sequence_list_of_arguments_named_item.
    def visitSequence_list_of_arguments_named_item(self, ctx:SystemVerilogParser.Sequence_list_of_arguments_named_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#sequence_list_of_arguments.
    def visitSequence_list_of_arguments(self, ctx:SystemVerilogParser.Sequence_list_of_argumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_arguments_named_item.
    def visitList_of_arguments_named_item(self, ctx:SystemVerilogParser.List_of_arguments_named_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_arguments.
    def visitList_of_arguments(self, ctx:SystemVerilogParser.List_of_argumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#primary_literal.
    def visitPrimary_literal(self, ctx:SystemVerilogParser.Primary_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#type_reference.
    def visitType_reference(self, ctx:SystemVerilogParser.Type_referenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#package_scope.
    def visitPackage_scope(self, ctx:SystemVerilogParser.Package_scopeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#ps_identifier.
    def visitPs_identifier(self, ctx:SystemVerilogParser.Ps_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_parameter_value_assignments.
    def visitList_of_parameter_value_assignments(self, ctx:SystemVerilogParser.List_of_parameter_value_assignmentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#parameter_value_assignment.
    def visitParameter_value_assignment(self, ctx:SystemVerilogParser.Parameter_value_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#class_type.
    def visitClass_type(self, ctx:SystemVerilogParser.Class_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#class_scope.
    def visitClass_scope(self, ctx:SystemVerilogParser.Class_scopeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#range_expression.
    def visitRange_expression(self, ctx:SystemVerilogParser.Range_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#constant_range_expression.
    def visitConstant_range_expression(self, ctx:SystemVerilogParser.Constant_range_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#constant_mintypmax_expression.
    def visitConstant_mintypmax_expression(self, ctx:SystemVerilogParser.Constant_mintypmax_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#mintypmax_expression.
    def visitMintypmax_expression(self, ctx:SystemVerilogParser.Mintypmax_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#named_parameter_assignment.
    def visitNamed_parameter_assignment(self, ctx:SystemVerilogParser.Named_parameter_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryLit.
    def visitPrimaryLit(self, ctx:SystemVerilogParser.PrimaryLitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryRandomize.
    def visitPrimaryRandomize(self, ctx:SystemVerilogParser.PrimaryRandomizeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryAssig.
    def visitPrimaryAssig(self, ctx:SystemVerilogParser.PrimaryAssigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryBitSelect.
    def visitPrimaryBitSelect(self, ctx:SystemVerilogParser.PrimaryBitSelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryTfCall.
    def visitPrimaryTfCall(self, ctx:SystemVerilogParser.PrimaryTfCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryTypeRef.
    def visitPrimaryTypeRef(self, ctx:SystemVerilogParser.PrimaryTypeRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryCallArrayMethodNoArgs.
    def visitPrimaryCallArrayMethodNoArgs(self, ctx:SystemVerilogParser.PrimaryCallArrayMethodNoArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryCast.
    def visitPrimaryCast(self, ctx:SystemVerilogParser.PrimaryCastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryPar.
    def visitPrimaryPar(self, ctx:SystemVerilogParser.PrimaryParContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryCall.
    def visitPrimaryCall(self, ctx:SystemVerilogParser.PrimaryCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryRandomize2.
    def visitPrimaryRandomize2(self, ctx:SystemVerilogParser.PrimaryRandomize2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryDot.
    def visitPrimaryDot(self, ctx:SystemVerilogParser.PrimaryDotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryStreaming_concatenation.
    def visitPrimaryStreaming_concatenation(self, ctx:SystemVerilogParser.PrimaryStreaming_concatenationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryPath.
    def visitPrimaryPath(self, ctx:SystemVerilogParser.PrimaryPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryIndex.
    def visitPrimaryIndex(self, ctx:SystemVerilogParser.PrimaryIndexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryCallWith.
    def visitPrimaryCallWith(self, ctx:SystemVerilogParser.PrimaryCallWithContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryConcat.
    def visitPrimaryConcat(self, ctx:SystemVerilogParser.PrimaryConcatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#PrimaryCast2.
    def visitPrimaryCast2(self, ctx:SystemVerilogParser.PrimaryCast2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#constant_expression.
    def visitConstant_expression(self, ctx:SystemVerilogParser.Constant_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#Inc_or_dec_expressionPre.
    def visitInc_or_dec_expressionPre(self, ctx:SystemVerilogParser.Inc_or_dec_expressionPreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#Inc_or_dec_expressionPost.
    def visitInc_or_dec_expressionPost(self, ctx:SystemVerilogParser.Inc_or_dec_expressionPostContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#expression.
    def visitExpression(self, ctx:SystemVerilogParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#concatenation.
    def visitConcatenation(self, ctx:SystemVerilogParser.ConcatenationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dynamic_array_new.
    def visitDynamic_array_new(self, ctx:SystemVerilogParser.Dynamic_array_newContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#const_or_range_expression.
    def visitConst_or_range_expression(self, ctx:SystemVerilogParser.Const_or_range_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#variable_decl_assignment.
    def visitVariable_decl_assignment(self, ctx:SystemVerilogParser.Variable_decl_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#assignment_pattern_variable_lvalue.
    def visitAssignment_pattern_variable_lvalue(self, ctx:SystemVerilogParser.Assignment_pattern_variable_lvalueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#stream_operator.
    def visitStream_operator(self, ctx:SystemVerilogParser.Stream_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#slice_size.
    def visitSlice_size(self, ctx:SystemVerilogParser.Slice_sizeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#streaming_concatenation.
    def visitStreaming_concatenation(self, ctx:SystemVerilogParser.Streaming_concatenationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#stream_concatenation.
    def visitStream_concatenation(self, ctx:SystemVerilogParser.Stream_concatenationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#stream_expression.
    def visitStream_expression(self, ctx:SystemVerilogParser.Stream_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#array_range_expression.
    def visitArray_range_expression(self, ctx:SystemVerilogParser.Array_range_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#open_range_list.
    def visitOpen_range_list(self, ctx:SystemVerilogParser.Open_range_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#pattern.
    def visitPattern(self, ctx:SystemVerilogParser.PatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#assignment_pattern.
    def visitAssignment_pattern(self, ctx:SystemVerilogParser.Assignment_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#structure_pattern_key.
    def visitStructure_pattern_key(self, ctx:SystemVerilogParser.Structure_pattern_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#array_pattern_key.
    def visitArray_pattern_key(self, ctx:SystemVerilogParser.Array_pattern_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#assignment_pattern_key.
    def visitAssignment_pattern_key(self, ctx:SystemVerilogParser.Assignment_pattern_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#struct_union_member.
    def visitStruct_union_member(self, ctx:SystemVerilogParser.Struct_union_memberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#data_type_or_void.
    def visitData_type_or_void(self, ctx:SystemVerilogParser.Data_type_or_voidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#enum_name_declaration.
    def visitEnum_name_declaration(self, ctx:SystemVerilogParser.Enum_name_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#assignment_pattern_expression.
    def visitAssignment_pattern_expression(self, ctx:SystemVerilogParser.Assignment_pattern_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#assignment_pattern_expression_type.
    def visitAssignment_pattern_expression_type(self, ctx:SystemVerilogParser.Assignment_pattern_expression_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#net_lvalue.
    def visitNet_lvalue(self, ctx:SystemVerilogParser.Net_lvalueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#variable_lvalue.
    def visitVariable_lvalue(self, ctx:SystemVerilogParser.Variable_lvalueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#solve_before_list.
    def visitSolve_before_list(self, ctx:SystemVerilogParser.Solve_before_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#constraint_block_item.
    def visitConstraint_block_item(self, ctx:SystemVerilogParser.Constraint_block_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#constraint_expression.
    def visitConstraint_expression(self, ctx:SystemVerilogParser.Constraint_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#uniqueness_constraint.
    def visitUniqueness_constraint(self, ctx:SystemVerilogParser.Uniqueness_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#constraint_set.
    def visitConstraint_set(self, ctx:SystemVerilogParser.Constraint_setContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#randomize_call.
    def visitRandomize_call(self, ctx:SystemVerilogParser.Randomize_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#module_header_common.
    def visitModule_header_common(self, ctx:SystemVerilogParser.Module_header_commonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#module_declaration.
    def visitModule_declaration(self, ctx:SystemVerilogParser.Module_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#module_keyword.
    def visitModule_keyword(self, ctx:SystemVerilogParser.Module_keywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#net_port_type.
    def visitNet_port_type(self, ctx:SystemVerilogParser.Net_port_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#var_data_type.
    def visitVar_data_type(self, ctx:SystemVerilogParser.Var_data_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#net_or_var_data_type.
    def visitNet_or_var_data_type(self, ctx:SystemVerilogParser.Net_or_var_data_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_defparam_assignments.
    def visitList_of_defparam_assignments(self, ctx:SystemVerilogParser.List_of_defparam_assignmentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_net_decl_assignments.
    def visitList_of_net_decl_assignments(self, ctx:SystemVerilogParser.List_of_net_decl_assignmentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_specparam_assignments.
    def visitList_of_specparam_assignments(self, ctx:SystemVerilogParser.List_of_specparam_assignmentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_variable_decl_assignments.
    def visitList_of_variable_decl_assignments(self, ctx:SystemVerilogParser.List_of_variable_decl_assignmentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_variable_identifiers_item.
    def visitList_of_variable_identifiers_item(self, ctx:SystemVerilogParser.List_of_variable_identifiers_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_variable_identifiers.
    def visitList_of_variable_identifiers(self, ctx:SystemVerilogParser.List_of_variable_identifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_variable_port_identifiers.
    def visitList_of_variable_port_identifiers(self, ctx:SystemVerilogParser.List_of_variable_port_identifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#defparam_assignment.
    def visitDefparam_assignment(self, ctx:SystemVerilogParser.Defparam_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#net_decl_assignment.
    def visitNet_decl_assignment(self, ctx:SystemVerilogParser.Net_decl_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#specparam_assignment.
    def visitSpecparam_assignment(self, ctx:SystemVerilogParser.Specparam_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#error_limit_value.
    def visitError_limit_value(self, ctx:SystemVerilogParser.Error_limit_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#reject_limit_value.
    def visitReject_limit_value(self, ctx:SystemVerilogParser.Reject_limit_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#pulse_control_specparam.
    def visitPulse_control_specparam(self, ctx:SystemVerilogParser.Pulse_control_specparamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#identifier_doted_index_at_end.
    def visitIdentifier_doted_index_at_end(self, ctx:SystemVerilogParser.Identifier_doted_index_at_endContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#specify_terminal_descriptor.
    def visitSpecify_terminal_descriptor(self, ctx:SystemVerilogParser.Specify_terminal_descriptorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#specify_input_terminal_descriptor.
    def visitSpecify_input_terminal_descriptor(self, ctx:SystemVerilogParser.Specify_input_terminal_descriptorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#specify_output_terminal_descriptor.
    def visitSpecify_output_terminal_descriptor(self, ctx:SystemVerilogParser.Specify_output_terminal_descriptorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#specify_item.
    def visitSpecify_item(self, ctx:SystemVerilogParser.Specify_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#pulsestyle_declaration.
    def visitPulsestyle_declaration(self, ctx:SystemVerilogParser.Pulsestyle_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#showcancelled_declaration.
    def visitShowcancelled_declaration(self, ctx:SystemVerilogParser.Showcancelled_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#path_declaration.
    def visitPath_declaration(self, ctx:SystemVerilogParser.Path_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#simple_path_declaration.
    def visitSimple_path_declaration(self, ctx:SystemVerilogParser.Simple_path_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#path_delay_value.
    def visitPath_delay_value(self, ctx:SystemVerilogParser.Path_delay_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_path_outputs.
    def visitList_of_path_outputs(self, ctx:SystemVerilogParser.List_of_path_outputsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_path_inputs.
    def visitList_of_path_inputs(self, ctx:SystemVerilogParser.List_of_path_inputsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_paths.
    def visitList_of_paths(self, ctx:SystemVerilogParser.List_of_pathsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_path_delay_expressions.
    def visitList_of_path_delay_expressions(self, ctx:SystemVerilogParser.List_of_path_delay_expressionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#t_path_delay_expression.
    def visitT_path_delay_expression(self, ctx:SystemVerilogParser.T_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#trise_path_delay_expression.
    def visitTrise_path_delay_expression(self, ctx:SystemVerilogParser.Trise_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#tfall_path_delay_expression.
    def visitTfall_path_delay_expression(self, ctx:SystemVerilogParser.Tfall_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#tz_path_delay_expression.
    def visitTz_path_delay_expression(self, ctx:SystemVerilogParser.Tz_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#t01_path_delay_expression.
    def visitT01_path_delay_expression(self, ctx:SystemVerilogParser.T01_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#t10_path_delay_expression.
    def visitT10_path_delay_expression(self, ctx:SystemVerilogParser.T10_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#t0z_path_delay_expression.
    def visitT0z_path_delay_expression(self, ctx:SystemVerilogParser.T0z_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#tz1_path_delay_expression.
    def visitTz1_path_delay_expression(self, ctx:SystemVerilogParser.Tz1_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#t1z_path_delay_expression.
    def visitT1z_path_delay_expression(self, ctx:SystemVerilogParser.T1z_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#tz0_path_delay_expression.
    def visitTz0_path_delay_expression(self, ctx:SystemVerilogParser.Tz0_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#t0x_path_delay_expression.
    def visitT0x_path_delay_expression(self, ctx:SystemVerilogParser.T0x_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#tx1_path_delay_expression.
    def visitTx1_path_delay_expression(self, ctx:SystemVerilogParser.Tx1_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#t1x_path_delay_expression.
    def visitT1x_path_delay_expression(self, ctx:SystemVerilogParser.T1x_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#tx0_path_delay_expression.
    def visitTx0_path_delay_expression(self, ctx:SystemVerilogParser.Tx0_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#txz_path_delay_expression.
    def visitTxz_path_delay_expression(self, ctx:SystemVerilogParser.Txz_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#tzx_path_delay_expression.
    def visitTzx_path_delay_expression(self, ctx:SystemVerilogParser.Tzx_path_delay_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#parallel_path_description.
    def visitParallel_path_description(self, ctx:SystemVerilogParser.Parallel_path_descriptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#full_path_description.
    def visitFull_path_description(self, ctx:SystemVerilogParser.Full_path_descriptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#identifier_list.
    def visitIdentifier_list(self, ctx:SystemVerilogParser.Identifier_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#specparam_declaration.
    def visitSpecparam_declaration(self, ctx:SystemVerilogParser.Specparam_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#edge_sensitive_path_declaration.
    def visitEdge_sensitive_path_declaration(self, ctx:SystemVerilogParser.Edge_sensitive_path_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#parallel_edge_sensitive_path_description.
    def visitParallel_edge_sensitive_path_description(self, ctx:SystemVerilogParser.Parallel_edge_sensitive_path_descriptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#full_edge_sensitive_path_description.
    def visitFull_edge_sensitive_path_description(self, ctx:SystemVerilogParser.Full_edge_sensitive_path_descriptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#data_source_expression.
    def visitData_source_expression(self, ctx:SystemVerilogParser.Data_source_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#data_declaration.
    def visitData_declaration(self, ctx:SystemVerilogParser.Data_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#module_path_expression.
    def visitModule_path_expression(self, ctx:SystemVerilogParser.Module_path_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#state_dependent_path_declaration.
    def visitState_dependent_path_declaration(self, ctx:SystemVerilogParser.State_dependent_path_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#package_export_declaration.
    def visitPackage_export_declaration(self, ctx:SystemVerilogParser.Package_export_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#genvar_declaration.
    def visitGenvar_declaration(self, ctx:SystemVerilogParser.Genvar_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#net_declaration.
    def visitNet_declaration(self, ctx:SystemVerilogParser.Net_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#parameter_port_list.
    def visitParameter_port_list(self, ctx:SystemVerilogParser.Parameter_port_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#parameter_port_declaration.
    def visitParameter_port_declaration(self, ctx:SystemVerilogParser.Parameter_port_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_port_declarations_ansi_item.
    def visitList_of_port_declarations_ansi_item(self, ctx:SystemVerilogParser.List_of_port_declarations_ansi_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_port_declarations.
    def visitList_of_port_declarations(self, ctx:SystemVerilogParser.List_of_port_declarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#nonansi_port_declaration.
    def visitNonansi_port_declaration(self, ctx:SystemVerilogParser.Nonansi_port_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#nonansi_port.
    def visitNonansi_port(self, ctx:SystemVerilogParser.Nonansi_portContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#nonansi_port__expr.
    def visitNonansi_port__expr(self, ctx:SystemVerilogParser.Nonansi_port__exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#port_identifier.
    def visitPort_identifier(self, ctx:SystemVerilogParser.Port_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#ansi_port_declaration.
    def visitAnsi_port_declaration(self, ctx:SystemVerilogParser.Ansi_port_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#system_timing_check.
    def visitSystem_timing_check(self, ctx:SystemVerilogParser.System_timing_checkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dolar_setup_timing_check.
    def visitDolar_setup_timing_check(self, ctx:SystemVerilogParser.Dolar_setup_timing_checkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dolar_hold_timing_check.
    def visitDolar_hold_timing_check(self, ctx:SystemVerilogParser.Dolar_hold_timing_checkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dolar_setuphold_timing_check.
    def visitDolar_setuphold_timing_check(self, ctx:SystemVerilogParser.Dolar_setuphold_timing_checkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dolar_recovery_timing_check.
    def visitDolar_recovery_timing_check(self, ctx:SystemVerilogParser.Dolar_recovery_timing_checkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dolar_removal_timing_check.
    def visitDolar_removal_timing_check(self, ctx:SystemVerilogParser.Dolar_removal_timing_checkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dolar_recrem_timing_check.
    def visitDolar_recrem_timing_check(self, ctx:SystemVerilogParser.Dolar_recrem_timing_checkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dolar_skew_timing_check.
    def visitDolar_skew_timing_check(self, ctx:SystemVerilogParser.Dolar_skew_timing_checkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dolar_timeskew_timing_check.
    def visitDolar_timeskew_timing_check(self, ctx:SystemVerilogParser.Dolar_timeskew_timing_checkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dolar_fullskew_timing_check.
    def visitDolar_fullskew_timing_check(self, ctx:SystemVerilogParser.Dolar_fullskew_timing_checkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dolar_period_timing_check.
    def visitDolar_period_timing_check(self, ctx:SystemVerilogParser.Dolar_period_timing_checkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dolar_width_timing_check.
    def visitDolar_width_timing_check(self, ctx:SystemVerilogParser.Dolar_width_timing_checkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dolar_nochange_timing_check.
    def visitDolar_nochange_timing_check(self, ctx:SystemVerilogParser.Dolar_nochange_timing_checkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#timecheck_condition.
    def visitTimecheck_condition(self, ctx:SystemVerilogParser.Timecheck_conditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#controlled_reference_event.
    def visitControlled_reference_event(self, ctx:SystemVerilogParser.Controlled_reference_eventContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#delayed_reference.
    def visitDelayed_reference(self, ctx:SystemVerilogParser.Delayed_referenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#end_edge_offset.
    def visitEnd_edge_offset(self, ctx:SystemVerilogParser.End_edge_offsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#event_based_flag.
    def visitEvent_based_flag(self, ctx:SystemVerilogParser.Event_based_flagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#notifier.
    def visitNotifier(self, ctx:SystemVerilogParser.NotifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#remain_active_flag.
    def visitRemain_active_flag(self, ctx:SystemVerilogParser.Remain_active_flagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#timestamp_condition.
    def visitTimestamp_condition(self, ctx:SystemVerilogParser.Timestamp_conditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#start_edge_offset.
    def visitStart_edge_offset(self, ctx:SystemVerilogParser.Start_edge_offsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#threshold.
    def visitThreshold(self, ctx:SystemVerilogParser.ThresholdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#timing_check_limit.
    def visitTiming_check_limit(self, ctx:SystemVerilogParser.Timing_check_limitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#timing_check_event.
    def visitTiming_check_event(self, ctx:SystemVerilogParser.Timing_check_eventContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#timing_check_condition.
    def visitTiming_check_condition(self, ctx:SystemVerilogParser.Timing_check_conditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#scalar_timing_check_condition.
    def visitScalar_timing_check_condition(self, ctx:SystemVerilogParser.Scalar_timing_check_conditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#controlled_timing_check_event.
    def visitControlled_timing_check_event(self, ctx:SystemVerilogParser.Controlled_timing_check_eventContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#function_data_type_or_implicit.
    def visitFunction_data_type_or_implicit(self, ctx:SystemVerilogParser.Function_data_type_or_implicitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#extern_tf_declaration.
    def visitExtern_tf_declaration(self, ctx:SystemVerilogParser.Extern_tf_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#function_declaration.
    def visitFunction_declaration(self, ctx:SystemVerilogParser.Function_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#task_prototype.
    def visitTask_prototype(self, ctx:SystemVerilogParser.Task_prototypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#function_prototype.
    def visitFunction_prototype(self, ctx:SystemVerilogParser.Function_prototypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dpi_import_export.
    def visitDpi_import_export(self, ctx:SystemVerilogParser.Dpi_import_exportContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dpi_function_import_property.
    def visitDpi_function_import_property(self, ctx:SystemVerilogParser.Dpi_function_import_propertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#dpi_task_import_property.
    def visitDpi_task_import_property(self, ctx:SystemVerilogParser.Dpi_task_import_propertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#task_and_function_declaration_common.
    def visitTask_and_function_declaration_common(self, ctx:SystemVerilogParser.Task_and_function_declaration_commonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#task_declaration.
    def visitTask_declaration(self, ctx:SystemVerilogParser.Task_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#method_prototype.
    def visitMethod_prototype(self, ctx:SystemVerilogParser.Method_prototypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#extern_constraint_declaration.
    def visitExtern_constraint_declaration(self, ctx:SystemVerilogParser.Extern_constraint_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#constraint_block.
    def visitConstraint_block(self, ctx:SystemVerilogParser.Constraint_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#checker_port_list.
    def visitChecker_port_list(self, ctx:SystemVerilogParser.Checker_port_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#checker_port_item.
    def visitChecker_port_item(self, ctx:SystemVerilogParser.Checker_port_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#checker_port_direction.
    def visitChecker_port_direction(self, ctx:SystemVerilogParser.Checker_port_directionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#checker_declaration.
    def visitChecker_declaration(self, ctx:SystemVerilogParser.Checker_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#class_declaration.
    def visitClass_declaration(self, ctx:SystemVerilogParser.Class_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#always_construct.
    def visitAlways_construct(self, ctx:SystemVerilogParser.Always_constructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#interface_class_type.
    def visitInterface_class_type(self, ctx:SystemVerilogParser.Interface_class_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#interface_class_declaration.
    def visitInterface_class_declaration(self, ctx:SystemVerilogParser.Interface_class_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#interface_class_item.
    def visitInterface_class_item(self, ctx:SystemVerilogParser.Interface_class_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#interface_class_method.
    def visitInterface_class_method(self, ctx:SystemVerilogParser.Interface_class_methodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#package_declaration.
    def visitPackage_declaration(self, ctx:SystemVerilogParser.Package_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#package_item.
    def visitPackage_item(self, ctx:SystemVerilogParser.Package_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#program_declaration.
    def visitProgram_declaration(self, ctx:SystemVerilogParser.Program_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#program_header.
    def visitProgram_header(self, ctx:SystemVerilogParser.Program_headerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#program_item.
    def visitProgram_item(self, ctx:SystemVerilogParser.Program_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#non_port_program_item.
    def visitNon_port_program_item(self, ctx:SystemVerilogParser.Non_port_program_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#anonymous_program.
    def visitAnonymous_program(self, ctx:SystemVerilogParser.Anonymous_programContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#anonymous_program_item.
    def visitAnonymous_program_item(self, ctx:SystemVerilogParser.Anonymous_program_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#sequence_declaration.
    def visitSequence_declaration(self, ctx:SystemVerilogParser.Sequence_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#sequence_port_list.
    def visitSequence_port_list(self, ctx:SystemVerilogParser.Sequence_port_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#sequence_port_item.
    def visitSequence_port_item(self, ctx:SystemVerilogParser.Sequence_port_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#property_declaration.
    def visitProperty_declaration(self, ctx:SystemVerilogParser.Property_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#property_port_list.
    def visitProperty_port_list(self, ctx:SystemVerilogParser.Property_port_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#property_port_item.
    def visitProperty_port_item(self, ctx:SystemVerilogParser.Property_port_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#continuous_assign.
    def visitContinuous_assign(self, ctx:SystemVerilogParser.Continuous_assignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#checker_or_generate_item.
    def visitChecker_or_generate_item(self, ctx:SystemVerilogParser.Checker_or_generate_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#constraint_prototype.
    def visitConstraint_prototype(self, ctx:SystemVerilogParser.Constraint_prototypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#class_constraint.
    def visitClass_constraint(self, ctx:SystemVerilogParser.Class_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#constraint_declaration.
    def visitConstraint_declaration(self, ctx:SystemVerilogParser.Constraint_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#class_constructor_declaration.
    def visitClass_constructor_declaration(self, ctx:SystemVerilogParser.Class_constructor_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#class_property.
    def visitClass_property(self, ctx:SystemVerilogParser.Class_propertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#class_method.
    def visitClass_method(self, ctx:SystemVerilogParser.Class_methodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#class_constructor_prototype.
    def visitClass_constructor_prototype(self, ctx:SystemVerilogParser.Class_constructor_prototypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#class_item.
    def visitClass_item(self, ctx:SystemVerilogParser.Class_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#parameter_override.
    def visitParameter_override(self, ctx:SystemVerilogParser.Parameter_overrideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#gate_instantiation.
    def visitGate_instantiation(self, ctx:SystemVerilogParser.Gate_instantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#enable_gate_or_mos_switch_or_cmos_switch_instance.
    def visitEnable_gate_or_mos_switch_or_cmos_switch_instance(self, ctx:SystemVerilogParser.Enable_gate_or_mos_switch_or_cmos_switch_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#n_input_gate_instance.
    def visitN_input_gate_instance(self, ctx:SystemVerilogParser.N_input_gate_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#n_output_gate_instance.
    def visitN_output_gate_instance(self, ctx:SystemVerilogParser.N_output_gate_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#pass_switch_instance.
    def visitPass_switch_instance(self, ctx:SystemVerilogParser.Pass_switch_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#pass_enable_switch_instance.
    def visitPass_enable_switch_instance(self, ctx:SystemVerilogParser.Pass_enable_switch_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#pull_gate_instance.
    def visitPull_gate_instance(self, ctx:SystemVerilogParser.Pull_gate_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#pulldown_strength.
    def visitPulldown_strength(self, ctx:SystemVerilogParser.Pulldown_strengthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#pullup_strength.
    def visitPullup_strength(self, ctx:SystemVerilogParser.Pullup_strengthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#enable_terminal.
    def visitEnable_terminal(self, ctx:SystemVerilogParser.Enable_terminalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#inout_terminal.
    def visitInout_terminal(self, ctx:SystemVerilogParser.Inout_terminalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#input_terminal.
    def visitInput_terminal(self, ctx:SystemVerilogParser.Input_terminalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#output_terminal.
    def visitOutput_terminal(self, ctx:SystemVerilogParser.Output_terminalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#udp_instantiation.
    def visitUdp_instantiation(self, ctx:SystemVerilogParser.Udp_instantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#udp_instance.
    def visitUdp_instance(self, ctx:SystemVerilogParser.Udp_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#udp_instance_body.
    def visitUdp_instance_body(self, ctx:SystemVerilogParser.Udp_instance_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#module_or_interface_or_program_or_udp_instantiation.
    def visitModule_or_interface_or_program_or_udp_instantiation(self, ctx:SystemVerilogParser.Module_or_interface_or_program_or_udp_instantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#hierarchical_instance.
    def visitHierarchical_instance(self, ctx:SystemVerilogParser.Hierarchical_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#list_of_port_connections.
    def visitList_of_port_connections(self, ctx:SystemVerilogParser.List_of_port_connectionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#ordered_port_connection.
    def visitOrdered_port_connection(self, ctx:SystemVerilogParser.Ordered_port_connectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#named_port_connection.
    def visitNamed_port_connection(self, ctx:SystemVerilogParser.Named_port_connectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#bind_directive.
    def visitBind_directive(self, ctx:SystemVerilogParser.Bind_directiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#bind_target_instance.
    def visitBind_target_instance(self, ctx:SystemVerilogParser.Bind_target_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#bind_target_instance_list.
    def visitBind_target_instance_list(self, ctx:SystemVerilogParser.Bind_target_instance_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#bind_instantiation.
    def visitBind_instantiation(self, ctx:SystemVerilogParser.Bind_instantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#config_declaration.
    def visitConfig_declaration(self, ctx:SystemVerilogParser.Config_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#design_statement.
    def visitDesign_statement(self, ctx:SystemVerilogParser.Design_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#config_rule_statement.
    def visitConfig_rule_statement(self, ctx:SystemVerilogParser.Config_rule_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#inst_clause.
    def visitInst_clause(self, ctx:SystemVerilogParser.Inst_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#inst_name.
    def visitInst_name(self, ctx:SystemVerilogParser.Inst_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#cell_clause.
    def visitCell_clause(self, ctx:SystemVerilogParser.Cell_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#liblist_clause.
    def visitLiblist_clause(self, ctx:SystemVerilogParser.Liblist_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#use_clause.
    def visitUse_clause(self, ctx:SystemVerilogParser.Use_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#net_alias.
    def visitNet_alias(self, ctx:SystemVerilogParser.Net_aliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#specify_block.
    def visitSpecify_block(self, ctx:SystemVerilogParser.Specify_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#generate_region.
    def visitGenerate_region(self, ctx:SystemVerilogParser.Generate_regionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#genvar_expression.
    def visitGenvar_expression(self, ctx:SystemVerilogParser.Genvar_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#loop_generate_construct.
    def visitLoop_generate_construct(self, ctx:SystemVerilogParser.Loop_generate_constructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#genvar_initialization.
    def visitGenvar_initialization(self, ctx:SystemVerilogParser.Genvar_initializationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#genvar_iteration.
    def visitGenvar_iteration(self, ctx:SystemVerilogParser.Genvar_iterationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#conditional_generate_construct.
    def visitConditional_generate_construct(self, ctx:SystemVerilogParser.Conditional_generate_constructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#if_generate_construct.
    def visitIf_generate_construct(self, ctx:SystemVerilogParser.If_generate_constructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#case_generate_construct.
    def visitCase_generate_construct(self, ctx:SystemVerilogParser.Case_generate_constructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#case_generate_item.
    def visitCase_generate_item(self, ctx:SystemVerilogParser.Case_generate_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#generate_begin_end_block.
    def visitGenerate_begin_end_block(self, ctx:SystemVerilogParser.Generate_begin_end_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#generate_item.
    def visitGenerate_item(self, ctx:SystemVerilogParser.Generate_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#program_generate_item.
    def visitProgram_generate_item(self, ctx:SystemVerilogParser.Program_generate_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#module_or_generate_or_interface_or_checker_item.
    def visitModule_or_generate_or_interface_or_checker_item(self, ctx:SystemVerilogParser.Module_or_generate_or_interface_or_checker_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#module_or_generate_or_interface_item.
    def visitModule_or_generate_or_interface_item(self, ctx:SystemVerilogParser.Module_or_generate_or_interface_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#module_or_generate_item.
    def visitModule_or_generate_item(self, ctx:SystemVerilogParser.Module_or_generate_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#elaboration_system_task.
    def visitElaboration_system_task(self, ctx:SystemVerilogParser.Elaboration_system_taskContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#module_item_item.
    def visitModule_item_item(self, ctx:SystemVerilogParser.Module_item_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemVerilogParser#module_item.
    def visitModule_item(self, ctx:SystemVerilogParser.Module_itemContext):
        return self.visitChildren(ctx)



del SystemVerilogParser