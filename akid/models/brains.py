from akid import Brain
from akid.layers import (
    ConvolutionLayer,
    PoolingLayer,
    ReLULayer,
    InnerProductLayer,
    SoftmaxWithLossLayer,
    LRNLayer,
    BatchNormalizationLayer,
    DropoutLayer,
    MergeLayer,
    ReshapeLayer,
    PaddingLayer,
    CollapseOutLayer,
    GroupSoftmaxLayer
)


class AlexNet(Brain):
    """
    A class for alex net specifically.
    """
    def __init__(self, **kwargs):
        super(AlexNet, self).__init__(**kwargs)

        self.attach(ConvolutionLayer([5, 5],
                                     [1, 1, 1, 1],
                                     'SAME',
                                     init_para={
                                         "name": "truncated_normal",
                                         "stddev": 1e-4},
                                     wd={"type": "l2", "scale": 0},
                                     out_channel_num=64,
                                     name='conv1'))
        self.attach(ReLULayer(name='relu1'))
        self.attach(PoolingLayer([1, 3, 3, 1],
                                 [1, 2, 2, 1],
                                 'SAME',
                                 name='pool1'))
        self.attach(LRNLayer(name='norm1'))

        self.attach(ConvolutionLayer([5, 5],
                                     [1, 1, 1, 1],
                                     'SAME',
                                     initial_bias_value=0.1,
                                     init_para={
                                         "name": "truncated_normal",
                                         "stddev": 1e-4},
                                     wd={"type": "l2", "scale": 0},
                                     out_channel_num=64,
                                     name='conv2'))
        self.attach(ReLULayer(name='relu2'))
        self.attach(LRNLayer(name='norm2'))
        self.attach(PoolingLayer([1, 3, 3, 1],
                                 [1, 2, 2, 1],
                                 'SAME',
                                 name='pool2'))
        self.attach(InnerProductLayer(initial_bias_value=0.1,
                                      init_para={
                                          "name": "truncated_normal",
                                          "stddev": 0.04},
                                      wd={"type": "l2", "scale": 0.004},
                                      out_channel_num=384,
                                      name='ip1'))
        self.attach(ReLULayer(name='relu3'))

        self.attach(InnerProductLayer(initial_bias_value=0.1,
                                      init_para={
                                          "name": "truncated_normal",
                                          "stddev": 0.04},
                                      wd={"type": "l2", "scale": 0.004},
                                      out_channel_num=192,
                                      name='ip2'))
        self.attach(InnerProductLayer(initial_bias_value=0,
                                      init_para={
                                          "name": "truncated_normal",
                                          "stddev": 1/192.0},
                                      wd={"type": "l2", "scale": 0},
                                      out_channel_num=10,
                                      name='softmax_linear'))

        self.attach(SoftmaxWithLossLayer(
            class_num=10,
            inputs=[{"name": "softmax_linear", "idxs": [0]},
                    {"name": "system_in", "idxs": [1]}],
            name="loss"))


class OneLayerBrain(Brain):
    def __init__(self, **kwargs):
        super(OneLayerBrain, self).__init__(**kwargs)
        self.attach(
            ConvolutionLayer(ksize=[5, 5],
                             strides=[1, 1, 1, 1],
                             padding="SAME",
                             out_channel_num=32,
                             name="conv1")
        )
        self.attach(ReLULayer(name="relu1"))
        self.attach(
            PoolingLayer(ksize=[1, 5, 5, 1],
                         strides=[1, 5, 5, 1],
                         padding="SAME",
                         name="pool1")
        )

        self.attach(InnerProductLayer(out_channel_num=10, name="ip1"))
        self.attach(SoftmaxWithLossLayer(
            class_num=10,
            inputs=[
                {"name": "ip1", "idxs": [0]},
                {"name": "system_in", "idxs": [1]}],
            name="loss"))


class LeNet(Brain):
    """
    A rough LeNet. It is supposed to copy the example from Caffe, but for the
    time being it has not been checked whether they are exactly the same.
    """
    def __init__(self, **kwargs):
        super(LeNet, self).__init__(**kwargs)
        self.attach(ConvolutionLayer(ksize=[5, 5],
                                     strides=[1, 1, 1, 1],
                                     padding="SAME",
                                     out_channel_num=32,
                                     name="conv1"))
        self.attach(ReLULayer(name="relu1"))
        self.attach(PoolingLayer(ksize=[1, 2, 2, 1],
                                 strides=[1, 2, 2, 1],
                                 padding="SAME",
                                 name="pool1"))

        self.attach(ConvolutionLayer(ksize=[5, 5],
                                     strides=[1, 1, 1, 1],
                                     padding="SAME",
                                     out_channel_num=64,
                                     name="conv2"))
        self.attach(ReLULayer(name="relu2"))
        self.attach(PoolingLayer(ksize=[1, 5, 5, 1],
                                 strides=[1, 2, 2, 1],
                                 padding="SAME",
                                 name="pool2"))

        self.attach(InnerProductLayer(out_channel_num=512, name="ip1"))
        self.attach(ReLULayer(name="relu3"))

        self.attach(InnerProductLayer(out_channel_num=10, name="ip2"))

        self.attach(SoftmaxWithLossLayer(
            class_num=10,
            inputs=[{"name": "ip2", "idxs": [0]},
                    {"name": "system_in", "idxs": [1]}],
            name="loss"))


class MnistTfTutorialNet(Brain):
    """
    A multiple layer network with parameters from the MNIST tutorial of
    tensorflow.
    """
    def __init__(self, **kwargs):
        super(MnistTfTutorialNet, self).__init__(**kwargs)
        self.attach(ConvolutionLayer(ksize=[5, 5],
                                     strides=[1, 1, 1, 1],
                                     padding="SAME",
                                     initial_bias_value=0.,
                                     init_para={"name": "truncated_normal",
                                                "stddev": 0.1},
                                     wd={"type": "l2", "scale": 5e-4},
                                     out_channel_num=32,
                                     name="conv1"))
        self.attach(ReLULayer(name="relu1"))
        self.attach(PoolingLayer(ksize=[1, 2, 2, 1],
                                 strides=[1, 2, 2, 1],
                                 padding="SAME",
                                 name="pool1"))

        self.attach(ConvolutionLayer(ksize=[5, 5],
                                     strides=[1, 1, 1, 1],
                                     padding="SAME",
                                     initial_bias_value=0.1,
                                     init_para={"name": "truncated_normal",
                                                "stddev": 0.1},
                                     wd={"type": "l2", "scale": 5e-4},
                                     out_channel_num=64,
                                     name="conv2"))
        self.attach(ReLULayer(name="relu2"))
        self.attach(PoolingLayer(ksize=[1, 5, 5, 1],
                                 strides=[1, 2, 2, 1],
                                 padding="SAME",
                                 name="pool2"))

        self.attach(InnerProductLayer(out_channel_num=512,
                                      initial_bias_value=0.1,
                                      init_para={"name": "truncated_normal",
                                                 "stddev": 0.1},
                                      wd={"type": "l2", "scale": 5e-4},
                                      name="ip1"))
        self.attach(ReLULayer(name="relu3"))
        self.attach(DropoutLayer(keep_prob=0.5, name="dropout1"))

        self.attach(InnerProductLayer(out_channel_num=10,
                                      initial_bias_value=0.1,
                                      init_para={"name": "truncated_normal",
                                                 "stddev": 0.1},
                                      wd={"type": "l2", "scale": 5e-4},
                                      name="ip2"))

        self.attach(SoftmaxWithLossLayer(
            class_num=10,
            inputs=[{"name": "ip2", "idxs": [0]},
                    {"name": "system_in", "idxs": [1]}],
            name="loss"))


class VGGNet(Brain):
    def __init__(self,
                 class_num=10,
                 padding="SAME",
                 loss_layer=None,
                 **kwargs):
        """
        Args:
            loss_layer: A tuple of (A python Class, A dict).
                The type of loss layer to use in this net. The first item is
                the class of the loss layer, and the second is extra parameters
                of this layer, besides `name`. If None, a softmax cross_entropy
                loss will be used.
        """
        super(VGGNet, self).__init__(**kwargs)
        self.padding = padding

        # The number counted by how many convolution layer has been applied. It
        # is used to give a easily told name to each layer.
        self.top_layer_No = 0

        self.attach_conv_bn_relu(64)
        self.attach(DropoutLayer(keep_prob=0.7,
                                 name="dropout{}".format(self.top_layer_No)))
        self.attach_conv_bn_relu(64)
        self.attach(PoolingLayer(ksize=[1, 2, 2, 1],
                                 strides=[1, 2, 2, 1],
                                 padding=self.padding,
                                 name="pool{}".format(self.top_layer_No)))

        self.attach_conv_bn_relu(128)
        self.attach(DropoutLayer(keep_prob=0.6,
                                 name="dropout{}".format(self.top_layer_No)))
        self.attach_conv_bn_relu(128)
        self.attach(PoolingLayer(ksize=[1, 2, 2, 1],
                                 strides=[1, 2, 2, 1],
                                 padding=self.padding,
                                 name="pool{}".format(self.top_layer_No)))

        self.attach_conv_bn_relu(256)
        self.attach(DropoutLayer(keep_prob=0.6,
                                 name="dropout{}".format(self.top_layer_No)))
        self.attach_conv_bn_relu(256)
        self.attach(DropoutLayer(keep_prob=0.6,
                                 name="dropout{}".format(self.top_layer_No)))
        self.attach_conv_bn_relu(256)
        self.attach(PoolingLayer(ksize=[1, 2, 2, 1],
                                 strides=[1, 2, 2, 1],
                                 padding=self.padding,
                                 name="pool{}".format(self.top_layer_No)))

        self.attach_conv_bn_relu(512)
        self.attach(DropoutLayer(keep_prob=0.6,
                                 name="dropout{}".format(self.top_layer_No)))
        self.attach_conv_bn_relu(512)
        self.attach(DropoutLayer(keep_prob=0.6,
                                 name="dropout{}".format(self.top_layer_No)))
        self.attach_conv_bn_relu(512)
        self.attach(PoolingLayer(ksize=[1, 2, 2, 1],
                                 strides=[1, 2, 2, 1],
                                 padding=self.padding,
                                 name="pool{}".format(self.top_layer_No)))

        self.top_layer_No += 1
        self.attach(DropoutLayer(keep_prob=0.5,
                                 name="dropout{}".format(self.top_layer_No)))
        self.attach(InnerProductLayer(out_channel_num=512,
                                      init_para={
                                          "name": "truncated_normal",
                                          "stddev": 1e-4},
                                      name="ip1"))
        self.attach(
            BatchNormalizationLayer(name="bn{}".format(self.top_layer_No)))
        self.attach(ReLULayer(name="relu{}".format(self.top_layer_No)))

        self.top_layer_No += 1
        self.attach(DropoutLayer(keep_prob=0.5,
                                 name="dropout{}".format(self.top_layer_No)))

        self.attach(InnerProductLayer(out_channel_num=class_num,
                                      init_para={
                                          "name": "truncated_normal",
                                          "stddev": 1e-4},
                                      name="ip2"))
        self.attach(
            BatchNormalizationLayer(name="bn{}".format(self.top_layer_No)))

        if loss_layer:
            self.attach(loss_layer[0](
                class_num=class_num,
                name="loss",
                **loss_layer[1]))
        else:
            self.attach(SoftmaxWithLossLayer(
                class_num=class_num,
                inputs=[{"name": "ip2", "idxs": [0]},
                        {"name": "system_in", "idxs": [1]}],
                name="loss"))

    def attach_conv_bn_relu(self, out_channel_num):
        """
        This method attach a block of layer, aka convolution, batch
        normalization, and ReLU, to the brain. It also maintains
        `top_layer_No`.
        """
        self.top_layer_No += 1
        self.attach(ConvolutionLayer([3, 3],
                                     [1, 1, 1, 1],
                                     padding=self.padding,
                                     init_para={
                                         "name": "truncated_normal",
                                         "stddev": 1e-4},
                                     wd={"type": "l2", "scale": 5e-4},
                                     out_channel_num=out_channel_num,
                                     name="conv{}".format(self.top_layer_No)))
        self.attach(BatchNormalizationLayer(
            name="bn{}".format(self.top_layer_No)))
        self.attach(ReLULayer(name="relu{}".format(self.top_layer_No)))


class ResNet(Brain):
    def __init__(self,
                 depth=28,
                 width=2,
                 class_num=10,
                 dropout_prob=None,
                 projection_shortcut=True,
                 use_gsmax=False,
                 group_size=4,
                 **kwargs):
        super(ResNet, self).__init__(**kwargs)

        self.depth = depth
        self.width = width
        self.class_num = class_num
        self.residual_block_No = 0
        self.dropout_prob = dropout_prob
        self.projection_shortcut = projection_shortcut
        self.use_bias = None
        self.use_gsmax = use_gsmax
        self.group_size = group_size

    def _attach_stack(self,
                      n_input_plane,
                      n_output_plane,
                      count,
                      stride,
                      act_before_residual,
                      block_type="basic"):
        if block_type == "basic":
            conv_params = [[(3, 3), stride, "SAME"],
                           [(3, 3), (1, 1), "SAME"]]
        elif block_type == "bottleneck":
            # The implementation of bottleneck layer is a little tricky, though
            # I think I make it clearer than Facebook's version that uses a
            # global variable. Besides that we choose the type of residual unit
            # using the string here, in the actual `_attach_block` method, the
            # `n_input_plane` and `n_output_plane` methods stick with their
            # essential meaning when not using a bottleneck unit. That's to say
            # the real channel number when 3X3 convolution is applied. The
            # enlarging of channel number happens internally, similar with how
            # it is done in the facebook version.
            conv_params = [[(1, 1), (1, 1), "SAME"],
                           [(3, 3), stride, "SAME"],
                           [(1, 1), (1, 1), "SAME"]]
        else:
            raise Exception("Block type {} is not supported.".format(block_type))

        self._attach_block(n_input_plane,
                           n_output_plane,
                           stride,
                           act_before_residual,
                           conv_params)
        for i in xrange(2, count+1):
            if block_type == "basic":
                conv_params = [[(3, 3), (1, 1), "SAME"],
                               [(3, 3), (1, 1), "SAME"]]
            elif block_type == "bottleneck":
                conv_params = [[(1, 1), (1, 1), "SAME"],
                               [(3, 3), (1, 1), "SAME"],
                               [(1, 1), (1, 1), "SAME"]]
            else:
                raise Exception("Block type {} is not supported.".format(block_type))

            self._attach_block(n_output_plane,
                               n_output_plane,
                               (1, 1),
                               False,
                               conv_params)

    def _attach_block(self,
                      n_input_plane,
                      n_output_plane,
                      stride,
                      act_before_residual,
                      conv_params):
        self.residual_block_No += 1

        main_branch_layer_name = self.blocks[-1].name

        is_bottleneck = False  # A flag for shortcut padding.
        for i, v in enumerate(conv_params):
            ksize, r_stride, padding = v
            self.attach(BatchNormalizationLayer(
                name="bn_{}_{}".format(self.residual_block_No, i)))

            if self.use_gsmax and n_input_plane > 16:
                self.attach(GroupSoftmaxLayer(
                    group_size=self.group_size*n_input_plane/160,
                    name="gsmax_{}_{}".format(self.residual_block_No, i)))
            else:
                self.attach(ReLULayer(name="relu_{}_{}".format(
                    self.residual_block_No, i)))

            if i == 0:
                if n_input_plane != n_output_plane and act_before_residual:
                    # At the first block of each BIG layer, two branches may
                    # share the same BN and activation function, thus bookkeep
                    # the branching layer name.
                    main_branch_layer_name = self.blocks[-1].name

            # We determine whether this is bottleneck layer by checking the
            # kernel size.
            if i == len(conv_params) - 1 and list(ksize) == [1, 1]:
                # This is the last layer of a bottleneck layer, we need to
                # increase the channel number back.
                is_bottleneck = True
                # In wide residual network, only bottleneck conv layer is
                # widened, thus the effect needs be offset back.
                out_channel_num = n_output_plane * 4 / self.width
            else:
                out_channel_num = n_output_plane

            if i != 0:
                if self.dropout_prob:
                    self.attach(DropoutLayer(
                        keep_prob=1-self.dropout_prob,
                        name="dropout_{}_{}".format(self.residual_block_No,
                                                    i)))
            self.attach(ConvolutionLayer(ksize,
                                         [1, r_stride[0], r_stride[1], 1],
                                         padding=padding,
                                         init_para={"name": "msra_init"},
                                         initial_bias_value=self.use_bias,
                                         wd=self.wd,
                                         out_channel_num=out_channel_num,
                                         name="conv_{}_{}".format(
                                             self.residual_block_No, i)))

        last_residual_layer_name = self.blocks[-1].name

        if n_input_plane != n_output_plane:
            if self.projection_shortcut:
                self.attach(ConvolutionLayer(
                    [1, 1],
                    [1, stride[0], stride[1], 1],
                    inputs=[{"name": main_branch_layer_name}],
                    padding="SAME",
                    init_para={"name": "msra_init"},
                    initial_bias_value=self.use_bias,
                    wd=self.wd,
                    out_channel_num=out_channel_num,
                    name="conv_{}_shortcut".format(self.residual_block_No)))
            else:
                _ = (1, stride[0], stride[1], 1)
                if is_bottleneck:
                    in_channel_num = n_input_plane * 4
                else:
                    in_channel_num = n_input_plane

                self.attach(PoolingLayer(
                    ksize=_,
                    strides=_,
                    inputs=[{"name": main_branch_layer_name}],
                    padding="VALID",
                    type="avg",
                    name="pool_{}_shortcut".format(self.residual_block_No)))
                self.attach(PaddingLayer(
                    padding=[0, 0, 0, (out_channel_num - in_channel_num) // 2],
                    name="pad_{}_shortcut".format(self.residual_block_No)))

            shortcut_layer_name = self.blocks[-1].name
        else:
            shortcut_layer_name = main_branch_layer_name

        self.attach(MergeLayer(inputs=[{"name": last_residual_layer_name},
                                       {"name": shortcut_layer_name}],
                               name="merge_{}".format(self.residual_block_No)))


class CifarResNet(ResNet):
    def __init__(self,
                 sub_class_multiplier_ratio=0.5,
                 h_loss=False,
                 **kwargs):
        super(CifarResNet, self).__init__(**kwargs)

        depth = self.depth

        assert((depth - 4) % 6 == 0)
        k = self.width
        n_stages = [16, 16*k, 32*k, 64*k]
        assert (depth - 4) % 6 is 0
        n = (depth - 4) / 6
        if self.projection_shortcut:
            act_before_residual = [True, True, True]
            self.wd = {"type": "l2", "scale": 5e-4}
        else:
            act_before_residual = [True, False, False]
            self.wd = {"type": "l2", "scale": 0.0002}

        self.attach(ConvolutionLayer([3, 3],
                                     [1, 1, 1, 1],
                                     padding="SAME",
                                     init_para={"name": "msra_init"},
                                     wd=self.wd,
                                     out_channel_num=16,
                                     initial_bias_value=self.use_bias,
                                     name="conv0"))

        self._attach_stack(n_input_plane=n_stages[0],
                           n_output_plane=n_stages[1],
                           count=n,
                           stride=(1, 1),
                           act_before_residual=act_before_residual[0])
        self._attach_stack(n_input_plane=n_stages[1],
                           n_output_plane=n_stages[2],
                           count=n,
                           stride=(2, 2),
                           act_before_residual=act_before_residual[1])
        self._attach_stack(n_input_plane=n_stages[2],
                           n_output_plane=n_stages[3],
                           count=n,
                           stride=(2, 2),
                           act_before_residual=act_before_residual[2])
        self.attach(BatchNormalizationLayer(name="bn_out"))
        if self.use_gsmax:
            self.attach(GroupSoftmaxLayer(
                group_size=self.group_size*640/160,
                name="gsmax_out"))
        else:
            self.attach(ReLULayer(name="relu_out"))
        self.attach(PoolingLayer(ksize=[1, 8, 8, 1],
                                 strides=[1, 1, 1, 1],
                                 padding="VALID",
                                 type="avg",
                                 name="global_pool"))
        self.attach(ReshapeLayer(name="reshape"))
        self.attach(InnerProductLayer(initial_bias_value=0,
                                      init_para={"name": "default"},
                                      wd=self.wd,
                                      out_channel_num=self.class_num,
                                      name='ip'))
        if h_loss:
            self.attach(SoftmaxWithLossLayer(
                class_num=self.class_num,
                multiplier=sub_class_multiplier_ratio,
                inputs=[{"name": "ip"},
                        {"name": "system_in", "idxs": [2]}],
                name="softmax"))
            self.attach(CollapseOutLayer(group_size=5,
                                         type="average_out",
                                         inputs=[
                                             {"name": "ip"}
                                         ],
                                         name="average_out"))
            self.attach(SoftmaxWithLossLayer(
                class_num=20,
                multiplier=1-sub_class_multiplier_ratio,
                inputs=[
                    {"name": "average_out"},
                    {"name": "system_in", "idxs": [1]}],
                name="super_class_loss"))
        else:
            self.attach(SoftmaxWithLossLayer(
                class_num=self.class_num,
                inputs=[{"name": "ip"},
                        {"name": "system_in", "idxs": [1]}],
                name="softmax"))


class ImagenetResNet(ResNet):
    def __init__(self, **kwargs):
        super(ImagenetResNet, self).__init__(**kwargs)

        k = self.width
        n_stages = [64, 64*k, 128*k, 256*k, 512*k]
        # Given imagenet needs a some non-regular conv-bn-relu-pool block at
        # the beginning of the branch, it is tailed by handle, and replaces the
        # first shared pre-activation block. The remaining shared
        # pre-activation block are still active.
        act_before_residual = [False, True, True, True]
        strides = [1, 2, 2, 2]
        # The configuration to train imagenet.
        cfg = {
         18  : [[2, 2, 2, 2], "basicblock"],
         34  : [[3, 4, 6, 3], "basicblock"],
         50  : [[3, 4, 6, 3], "bottleneck"],
         101 : [[3, 4, 23, 3], "bottleneck"],
         152 : [[3, 8, 36, 3], "bottleneck"],
         200 : [[3, 24, 36, 3], "bottleneck"],
        }
        n_depth, block_name = cfg[self.depth]
        self.wd = {"type": "l2", "scale": 1e-4}

        self.attach(ConvolutionLayer([7, 7],
                                     [1, 2, 2, 1],
                                     padding="SAME",
                                     init_para={"name": "msra_init"},
                                     wd=self.wd,
                                     out_channel_num=64,
                                     initial_bias_value=self.use_bias,
                                     name="conv0"))
        self.attach(BatchNormalizationLayer(name="bn0"))
        self.attach(ReLULayer(name="relu0"))
        self.attach(PoolingLayer(ksize=[1, 3, 3, 1],
                                 strides=[1, 2, 2, 1],
                                 padding="SAME",
                                 type="max",
                                 name="pool0"))
        for i in xrange(4):
            self._attach_stack(n_input_plane=n_stages[i],
                               n_output_plane=n_stages[i+1],
                               count=n_depth[i],
                               stride=(strides[i], strides[i]),
                               act_before_residual=act_before_residual[i],
                               block_type="bottleneck")

        self.attach(ReLULayer(name="relu_final"))
        self.attach(PoolingLayer(ksize=[1, 7, 7, 1],
                                 strides=[1, 1, 1, 1],
                                 padding="VALID",
                                 type="avg",
                                 name="global_pool"))
        self.attach(ReshapeLayer(name="reshape"))
        self.attach(InnerProductLayer(initial_bias_value=0,
                                      init_para={"name": "default"},
                                      wd=self.wd,
                                      out_channel_num=self.class_num,
                                      name='ip'))
        self.attach(SoftmaxWithLossLayer(
            class_num=self.class_num,
            inputs=[{"name": "ip"},
                    {"name": "system_in", "idxs": [1]}],
            name="softmax"))
